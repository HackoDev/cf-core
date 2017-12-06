from django.db import models
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerField
from model_utils import Choices

from .abstract import PositionModel

__all__ = [
    'SocialLink'
]


class SocialLink(PositionModel):

    SOCIAL_CHOICES = Choices(
        ('vk', "VK"),
        ('fb', "Facebook"),
        ('tw', "Twitter"),
        ('gplus', "Google+"),
        ('youtube', "Youtube"),
        ('instagram', "Instagram")
    )

    name = models.CharField(
        verbose_name=_('name'),
        max_length=512,
        choices=SOCIAL_CHOICES,
        default=''
    )
    url = models.URLField(verbose_name=_('url'), default='')
    icon = ThumbnailerField(verbose_name=_('icon'), upload_to='icons/social/')

    def __str__(self):
        return self.get_name_display()

    class Meta:
        ordering = ('position',)
        verbose_name = _('social link')
        verbose_name_plural = _('social links')
