from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from model_utils.models import TimeStampedModel

from .abstract import PositionModel

__all__ = [
    'SliderImage'
]


class SliderImage(PositionModel, TimeStampedModel):
    """
    Хранение изображений для слайдера отображаемого на главной странице.
    """

    image = ThumbnailerImageField("изображение", upload_to='sliders/')
    width = models.PositiveIntegerField("ширина", default=0,
                                        help_text="При 0 не обрезается")
    height = models.PositiveIntegerField("высота", default=0,
                                         help_text="При 0 не обрезается")
    crop = models.BooleanField("использовать crop", default=False)

    def __str__(self):
        return '{} {}'.format(self.id, self.image)

    class Meta:
        ordering = ('position',)
        verbose_name = "изображение для слайдера"
        verbose_name_plural = "изображения для слайдера"
