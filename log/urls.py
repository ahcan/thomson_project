from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/log$', views.log_list_json, name='log_json'),
    url(r'^api/open$', views.open_log_list_json, name='open_log_json'),
    url(r'^api/(?P<jobID>\d+)/$', views.log_by_jobID_list_json, name='jobID_log_json'),

    url(r'^$', views.get_log, name='log'),
    url(r'^open/$', views.get_open_log, name='open'),
    url(r'^(?P<job_id>\d+)/$', views.get_log_by_jobID, name='byjobid'),
]
