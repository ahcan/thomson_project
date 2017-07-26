from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/job/$', views.job_json, name='job_json'),
    url(r'^api/waiting/$', views.waiting_job_json, name='waiting_job_json'),
    url(r'^api/running/$', views.running_job_json, name='running_job_json'),
    url(r'^api/paused/$', views.paused_job_json, name='paused_job_json'),
    url(r'^api/completed/$', views.completed_job_json, name='completed_job_json'),
    url(r'^api/aborted/$', views.aborted_job_json, name='aborted_job_json'),

    url(r'^$', views.get_job, name='job'),
    url(r'^waiting/$', views.get_waiting_job, name='waiting'),
    url(r'^running/$', views.get_running_job, name='running'),
    url(r'^paused/$', views.get_paused_job, name='paused'),
    url(r'^completed/$', views.get_completed_job, name='completed'),
    url(r'^aborted/$', views.aborted_job_json, name='aborted'),
]
