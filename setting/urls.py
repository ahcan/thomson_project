from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^log/', include('log.urls')),
    url(r'^system/', include('system.urls')),
]
