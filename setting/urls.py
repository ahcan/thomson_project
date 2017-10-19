from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^log/', include('log.urls')),
    url(r'^system/', include('system.urls')),
    url(r'^workflow/', include('workflow.urls')),
    url(r'^job/', include('job.urls')),
    url(r'^schedule/', include('schedule.urls')),
]
