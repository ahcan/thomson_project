from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^datetime/$', views.datetime_json, name='datetime_json'),
    url(r'^mountpoint/$', views.mountpoint_list_json, name='mountpoint_json'),
]
