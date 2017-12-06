from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstract import PositionModel


__all__ = [
    'Status'
]


class Status(PositionModel):

    name = models.CharField(verbose_name=_('name'), max_length=512, default='')

    content_type = models.ForeignKey(
        "contenttypes.ContentType",
        verbose_name=_('content type'),
        related_name='+'
    )

    def __str__(self):
        return self.name

    @classmethod
    def get_for_model(cls, model_cls):
        return cls.objects.filter(
            content_type_id=ContentType.objects.get_for_model(model_cls).id
        )

    class Meta:
        unique_together = (('name', 'content_type'),)
        ordering = ('position',)
        verbose_name = _('status')
        verbose_name_plural = _('statuses')
