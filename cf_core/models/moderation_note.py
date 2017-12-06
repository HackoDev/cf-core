import logging
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.db import models
from model_utils.models import TimeStampedModel

from .. import managers

logger = logging.getLogger(__name__)

__all__ = [
    'ModerationNote'
]


def signal_create_handler(**kwargs):
    """
    Process object moderation, execute `process_moderate` method on new notes.
    """

    if kwargs['created']:
        kwargs['instance'].instance.process_moderate(kwargs['instance'])


class ModerationNote(TimeStampedModel):
    MODERATE_STATUS_CHOICES = managers.MODERATE_STATUS_CHOICES

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        verbose_name=_('content type')
    )

    object_id = models.PositiveIntegerField(verbose_name=_('object id'))

    is_available = models.NullBooleanField(
        verbose_name=_('is available'),
        default=MODERATE_STATUS_CHOICES.WAIT,
        choices=MODERATE_STATUS_CHOICES
    )

    last_seen = models.DateTimeField(verbose_name=_('seen time'),
                                     default=None, null=True)

    note = models.TextField(verbose_name=_('note'), default='')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name=_('created by'))

    instance = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '{status}: {instance}'.format(
            instance=self.instance,
            status=self.get_is_available_display()
        )

    class Meta:
        ordering = ['-created']
        verbose_name = _('moderation note')
        verbose_name_plural = _('moderation notes')


post_save.connect(signal_create_handler, sender=ModerationNote)
