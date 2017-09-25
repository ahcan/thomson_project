from django.conf.urls import url
from . import views

urlpatterns = [
    #Link get thomson datetime: /system/api/datetime
    url(r'^api/datetime/$', views.datetime_json, name='datetime_json'),
    #Link get thomson datetime: /system/api/mountpoint
    url(r'^api/mountpoint/$', views.mountpoint_list_json, name='mountpoint_json'),
    #Link get thomson info CPU, RAAM: /system/api/status
    url(r'^api/status/$', views.get_system_status_json, name='status_json'),
    #Link get job status: /system/api/jobstatus
    url(r'^api/jobstatus/$', views.get_job_status_json, name='jobstatus_json'),

    #Link get thomson info CPU, RAAM: /system/api/status
    url(r'^api/nstatus/$', views.get_nodes_status_json, name='nstatus_json'),

    #Link get thomson info CPU, RAAM: /system/api/<node_id>/
    url(r'^api/(?P<node_id>\d+)/$', views.get_node_job_json, name='node_json'),

    #Main template dashboard
    url(r'^$', views.get_system, name="system"),
]
