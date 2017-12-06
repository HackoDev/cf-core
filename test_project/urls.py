from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from cf_core.router import router
from cf_core.api.views import DictionaryViewSet

router.register('dictionaries', DictionaryViewSet, base_name='dictionaries')

urlpatterns = [
    url(r'^api/v1/', include(router.get_urls())),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
