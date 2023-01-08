from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import settings

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('', include('Panel.urls'), name='Shop'),
]
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
