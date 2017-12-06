from django.db import models
from django.utils.translation import ugettext_lazy as _

from cf_core.models.abstract import PositionModel

__all__ = [
    'Location'
]


class Location(PositionModel):
    name = models.CharField(_('name'), max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('position',)
        verbose_name = _('location')
        verbose_name_plural = _('locations')
