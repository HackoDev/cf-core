import logging
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save
from django.db import models
from model_utils.models import TimeStampedModel

from .. import managers

logger = logging.getLogger(__name__)

__all__ = [
    'ModerationNote'
]


class ModerationNote(TimeStampedModel):
    MODERATE_STATUS_CHOICES = managers.MODERATE_STATUS_CHOICES

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        verbose_name="тип объекта"
    )

    object_id = models.PositiveIntegerField("id объекта")

    is_available = models.NullBooleanField(
        "опубликован",
        default=MODERATE_STATUS_CHOICES.WAIT,
        choices=MODERATE_STATUS_CHOICES
    )

    last_seen = models.DateTimeField("последний просмотр",
                                     default=None, null=True)

    note = models.TextField("заметка", default='')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="модератор")

    instance = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '{status}: {instance}'.format(
            instance=self.instance,
            status=self.get_is_available_display()
        )

    @staticmethod
    def signal_create_handler(**kwargs):
        """
        Обработка состояния у объекта модерации,
        используется в качестве обработчика сигнала. 
        """

        if kwargs['created']:
            kwargs['instance'].instance.process_moderate(kwargs['instance'])

    class Meta:
        ordering = ['-created']
        verbose_name = "запись по модерации"
        verbose_name_plural = "записи по модерации"


post_save.connect(ModerationNote.signal_create_handler, sender=ModerationNote)
