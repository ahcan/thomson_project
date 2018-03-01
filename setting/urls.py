from django.conf.urls import include, url
from django.contrib import admin
from system.views import monitor
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^accounts/', include('accounts.urls')),
    # url(r'^accounts/', include('tf_urls')),
    url(r'^log/', include('log.urls')),
    url(r'^system/', include('system.urls')),
    url(r'^workflow/', include('workflow.urls')),
    url(r'^job/', include('job.urls')),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^$', monitor, name='home'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'', include(tf_urls)),
]
