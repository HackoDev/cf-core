from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from model_utils.models import TimeStampedModel
from .abstract import PositionModel

__all__ = [
    'Contact'
]


class Contact(PositionModel, TimeStampedModel):
    phone_number = PhoneNumberField(
        verbose_name=_('phone number'),
        max_length=526,
        default=''
    )

    address = models.CharField(_('address'), max_length=1024, default='')
    lat = models.FloatField(_('latitude'), default=0)
    lng = models.FloatField(_('longitude'), default=0)

    def __str__(self):
        return self.address

    class Meta:
        ordering = ('position',)
        verbose_name = _('address and contacts')
        verbose_name_plural = _('addressed and contacts')
