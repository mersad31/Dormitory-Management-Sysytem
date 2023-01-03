from django.contrib import admin
from django.urls import include, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
                  re_path('admin/', admin.site.urls),
                  re_path('', include('Panel.urls'), name='Shop'),
              ] + staticfiles_urlpatterns()
