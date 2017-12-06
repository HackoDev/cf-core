from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from .abstract import PositionModel

__all__ = [
    'ServiceRule'
]


class ServiceRule(PositionModel, TimeStampedModel):

    parent = models.ForeignKey(
        'self',
        verbose_name=_('parent'),
        related_name='child_rules',
        blank=True,
        null=True
    )

    text = models.CharField(_('text'), max_length=128, default='')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('position',)
        verbose_name = _('service rule')
        verbose_name_plural = _('service rules')
