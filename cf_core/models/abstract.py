import logging

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from model_utils import Choices

from .. import managers

__all__ = [
    'PositionModel',
    'BaseModerateModel'
]

logger = logging.getLogger(__name__)


class PositionModel(models.Model):
    """
    Базовая модель, используемая для позиционируемых сущностей.
    """

    position = models.PositiveIntegerField(
        "позиция",
        default=0,
        help_text="используется для сортировки"
    )

    class Meta:
        ordering = ('position',)
        abstract = True


class BaseModerateModel(models.Model):
    """
    Базовая модель используемая для сущностей, которым требуется модерация.
    """

    MODERATE_STATUS_CHOICES = managers.MODERATE_STATUS_CHOICES

    MODERATE_PROCESS_TYPES = Choices(
        ('', 'DONE', "Ожидание"),
        ('CHECK', "Отправлен на проверку"),
        ('APPLY', "Применяется")
    )

    is_available = models.NullBooleanField(
        "статус модерации",
        default=MODERATE_STATUS_CHOICES.WAIT,
        choices=MODERATE_STATUS_CHOICES
    )

    approved_at = models.DateTimeField("дата модерации", default=None,
                                       blank=True, null=True)

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="модератор",
        related_name='%(class)ss_granted_list',
        default=None,
        blank=True,
        null=True
    )

    process_status = models.CharField(
        "статус обработки модерации",
        default=MODERATE_PROCESS_TYPES.DONE,
        choices=MODERATE_PROCESS_TYPES,
        max_length=8,
        blank=True
    )

    objects = managers.ModerateManager()

    moderation_notes = GenericRelation('cf_core.ModerationNote')

    def process_moderate(self, moderation_note, commit=True):
        """
        Модерация объекта.Заложена возможность расширять данный метод, 
        переопределив его у наследников.
        
        :param moderation_note: core.ModerationNote instance
        :param commit: bool Используется при необходимости 
        сохранить объект в БД.
        :return: 
        """

        if self.process_status != self.MODERATE_PROCESS_TYPES.APPLY:
            self.process_status = self.MODERATE_PROCESS_TYPES.APPLY
            self.save(update_fields=['process_status'])

        self.is_available = moderation_note.is_available
        self.approved_at = timezone.now()
        self.approved_by = moderation_note.created_by

        if commit:
            self.process_status = self.MODERATE_PROCESS_TYPES.DONE
            self.save()

        logger.info("Object was moderated: {instance}#{pk} -> {status}".format(
            instance=type(self), pk=self.pk, status=self.is_available
        ))

    class Meta:
        abstract = True
