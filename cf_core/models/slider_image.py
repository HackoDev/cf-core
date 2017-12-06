from django.db import models
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from model_utils.models import TimeStampedModel

from .abstract import PositionModel

__all__ = [
    'SliderImage'
]


class SliderImage(PositionModel, TimeStampedModel):
    """
    Slider images on index page
    """

    image = ThumbnailerImageField(verbose_name=_('image'), upload_to='sliders/')
    width = models.PositiveIntegerField(verbose_name=_('width'), default=0,
                                        help_text=_('on 0 does not crop'))
    height = models.PositiveIntegerField(verbose_name=_('height'), default=0,
                                         help_text=_('on 0 does not crop'))
    crop = models.BooleanField("использовать crop", default=False)

    def __str__(self):
        return '{} {}'.format(self.id, self.image)

    class Meta:
        ordering = ('position',)
        verbose_name = _('slider image')
        verbose_name_plural = _('slider images')
