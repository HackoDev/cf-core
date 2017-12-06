import logging

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

from cf_core import managers

__all__ = [
    'PositionModel',
    'BaseModerateModel'
]

logger = logging.getLogger(__name__)


class PositionModel(models.Model):
    """
    Abstract model, would be used for positional models.
    """

    position = models.PositiveIntegerField(
        verbose_name=_('position'),
        default=0,
        help_text=_('would be used for ordering')
    )

    class Meta:
        ordering = ('position',)
        abstract = True


class BaseModerateModel(models.Model):
    """
    Abstract model for moderating models.
    """

    MODERATE_STATUS_CHOICES = managers.MODERATE_STATUS_CHOICES

    MODERATE_PROCESS_TYPES = Choices(
        ('', 'DONE', _('wait')),
        ('CHECK', _('checking')),
        ('APPLY', _('applying'))
    )

    is_available = models.NullBooleanField(
        verbose_name=_('moderation status'),
        default=MODERATE_STATUS_CHOICES.WAIT,
        choices=MODERATE_STATUS_CHOICES
    )

    approved_at = models.DateTimeField(
        verbose_name=_('approved at'),
        default=None,
        blank=True,
        null=True
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('approved by'),
        related_name='%(class)ss_granted_list',
        default=None,
        blank=True,
        null=True
    )

    process_status = models.CharField(
        verbose_name=_('moderation status'),
        default=MODERATE_PROCESS_TYPES.DONE,
        choices=MODERATE_PROCESS_TYPES,
        max_length=8,
        blank=True
    )

    objects = managers.ModerateManager()

    moderation_notes = GenericRelation('cf_core.ModerationNote')

    def process_moderate(self, moderation_note, commit=True):
        """
        Moderation object. Would be used for extending current method.
        
        :param moderation_note: core.ModerationNote instance
        :param commit: bool Save object into database
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
