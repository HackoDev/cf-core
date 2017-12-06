from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

from cf_core import managers
from cf_core.models.abstract import PositionModel

__all__ = [
    'Partner',
    'InformationPartner',
    'RegularPartner'
]


class Partner(PositionModel):
    BASE_TYPE = None

    TYPE_CHOICES = Choices(
        ('regular', 'REGULAR', _('regular')),
        ('info', 'INFO', _('info'))
    )

    base_type = models.CharField(
        verbose_name=_('type'),
        max_length=16,
        choices=TYPE_CHOICES,
        default=TYPE_CHOICES.REGULAR
    )

    name = models.CharField(verbose_name=_('name'), max_length=128, default='')
    icon = models.ImageField(verbose_name=_('icon'), upload_to='partners/')

    objects = managers.PartnerManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('position',)
        verbose_name = _('partner')
        verbose_name_plural = _('partners')

    def save(self, *args, **kwargs):
        self.base_type = self.BASE_TYPE
        super(Partner, self).save(*args, **kwargs)


class RegularPartner(Partner):
    BASE_TYPE = Partner.TYPE_CHOICES.REGULAR

    class Meta(Partner.Meta):
        proxy = True


class InformationPartner(Partner):
    BASE_TYPE = Partner.TYPE_CHOICES.INFO

    class Meta(Partner.Meta):
        proxy = True
