from django.conf.urls import url
from . import views

urlpatterns = [
    #Link get thomson datetime: /system/api/datetime
    url(r'^api/datetime/$', views.datetime_json, name='datetime_json'),
    #Link get thomson datetime: /system/api/mountpoint
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/mountpoint/$', views.mountpoint_list_json, name='mountpoint_json'),
    #Link get thomson info CPU, RAAM: /system/api/status
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/status/$', views.get_system_status_json, name='status_json'),
    #Link get job status: /system/api/jobstatus
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/jobstatus/$', views.get_job_status_json, name='jobstatus_json'),

    #Link get thomson info CPU, RAAM: /system/api/nodes
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/nstatus/$', views.get_nodes_status_json, name='nstatus_json'),

    #Link get thomson info CPU, RAAM: /system/api/<node_id>/
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/(?P<node_id>\d+)/$', views.get_node_job_json, name='node_json'),

    #Link redirect node detail
    url(r'^detail-node/(?P<node_id>\d+)/$',views.redirect_node, name='node_detail'),

    #Link monitor
    url(r'^monitor/$', views.monitor, name='monitor'),
    #Link get captcha
    url(r'^captcha/$',views.captcha, name='captcha'),
    # url(r'^check_captcha/$', views.check_captcha, name='check_captcha'),
    url(r'^test/$', views.test, name='test'),
    #Link get thomson info CPU, RAAM: /system/api/<node_id>/
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/license/$', views.get_license_json, name='license_json'),
    
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/db_node/$', views.get_db_node, name='db_node'),
    #Main template dashboard
    url(r'^(?P<thomson_name>\w+\-+\w+)/$', views.get_system, name="system"),
]
