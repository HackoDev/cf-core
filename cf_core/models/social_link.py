from django.db import models
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

    name = models.CharField("название", max_length=512, choices=SOCIAL_CHOICES,
                            default='')
    url = models.URLField("url", default='')
    icon = ThumbnailerField("иконка", upload_to='icons/social/')

    def __str__(self):
        return self.get_name_display()

    class Meta:
        ordering = ('position',)
        verbose_name = "ссылка на соц. сеть"
        verbose_name_plural = "ссылки на соц. сети"
