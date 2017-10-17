from django.contrib.contenttypes.models import ContentType
from django.db import models

from .abstract import PositionModel


__all__ = [
    'Status'
]


class Status(PositionModel):
    """
    Модель статуса, используется для статусов различных сущностей.
    """

    name = models.CharField("Статус", max_length=512, default='')

    content_type = models.ForeignKey(
        "contenttypes.ContentType",
        verbose_name='тип объекта',
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
        verbose_name = "статус"
        verbose_name_plural = "статус"
