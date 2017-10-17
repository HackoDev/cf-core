from django.db import models
from model_utils.models import TimeStampedModel

from .abstract import PositionModel

__all__ = [
    'ServiceRule'
]


class ServiceRule(PositionModel, TimeStampedModel):

    parent = models.ForeignKey(
        'self',
        verbose_name="родитель",
        related_name='child_rules',
        blank=True,
        null=True
    )

    text = models.CharField("текст", max_length=128, default='')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('position',)
        verbose_name = "правило сервиса"
        verbose_name_plural = "правила сервиса"
