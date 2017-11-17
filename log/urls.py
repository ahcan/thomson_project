from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/log$', views.get_log_list_json, name='log_api'),
    url(r'^api/(?P<job_id>\d+)/$', views.get_log_by_jobID_list_json, name='jobID_log_api'),

    #link show all logs template
    url(r'^$', views.get_log, name='log'),
]
