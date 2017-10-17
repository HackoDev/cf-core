from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'cf_core'
    verbose_name = _("Core")
