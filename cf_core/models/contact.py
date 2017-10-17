from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from model_utils.models import TimeStampedModel
from .abstract import PositionModel

__all__ = [
    'Contact'
]


class Contact(PositionModel, TimeStampedModel):
    phone_number = PhoneNumberField(
        verbose_name="телефон",
        max_length=526,
        default=''
    )

    address = models.CharField("текст", max_length=1024, default='')
    lat = models.FloatField("широта", default=0)
    lng = models.FloatField("долгота", default=0)

    def __str__(self):
        return self.address

    class Meta:
        ordering = ('-position',)
        verbose_name = "адреса и контакты филиалов"
        verbose_name_plural = "адреса и контакты филиалов"
