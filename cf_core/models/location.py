from django.db import models

__all__ = [
    'Location'
]


class Location(models.Model):
    name = models.CharField("название", max_length=1024)
    position = models.PositiveIntegerField("позиция", default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('position',)
        verbose_name = "местоположение"
        verbose_name_plural = "местоположения"
