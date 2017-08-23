from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/datetime/$', views.datetime_json, name='datetime_json'),
    url(r'^api/mountpoint/$', views.mountpoint_list_json, name='mountpoint_json'),
    url(r'^api/status/$', views.get_system_status_json, name='status_json'),
    url(r'^api/bladestatus/$', views.get_blade_status_json, name='bladestatus_json'),
    url(r'^api/jobstatus/$', views.get_job_status_json, name='jobstatus_json'),

    url(r'^datetime/$', views.get_datetime, name='datetime'),
    url(r'^mountpoint/$', views.get_mountpoint, name='mountpoint'),
    url(r'^status/$', views.get_system_status, name='status'),
    url(r'^bladestatus/$', views.get_blade_status, name='bladestatus'),
    url(r'^jobstatus/$', views.get_job_status, name='jobstatus'),

    url(r'^$', views.get_system, name="system"),
]
