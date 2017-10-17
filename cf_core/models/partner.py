from django.db import models
from model_utils import Choices

from .. import managers
from .abstract import PositionModel

__all__ = [
    'Partner',
    'InformationPartner',
    'RegularPartner'
]


class Partner(PositionModel):
    BASE_TYPE = None

    TYPE_CHOICES = Choices(
        ('regular', 'REGULAR', "обычный"),
        ('info', 'INFO', "информационный")
    )

    base_type = models.CharField(
        "тип партнера",
        max_length=16,
        choices=TYPE_CHOICES,
        default=TYPE_CHOICES.REGULAR
    )

    name = models.CharField("название", max_length=128, default='')
    icon = models.ImageField("иконка", upload_to='partners/')

    objects = managers.PartnerManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('position',)
        verbose_name = "партнер"
        verbose_name_plural = "партнеры"

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
