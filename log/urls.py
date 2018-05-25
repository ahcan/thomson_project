from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/log/$', views.get_logs, name='log_api'),
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/(?P<job_id>\d+)/$', views.get_log_by_jobID_list_json, name='jobID_log_api'),
    #link filter log by severity
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/filter/$', views.filter_log, name="filter_log"),
    #link show all logs template
    url(r'^(?P<thomson_name>\w+\-+\w+)/$', views.get_log, name='log'),
    url(r'^testcaptcha/$', views.test_captcha, name='captcha'),
    url(r'^api/captcha/$', views.get_captcha, name='getCaptcha'),
]
