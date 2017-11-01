from django.conf.urls import url
from . import views

urlpatterns = [
    #link response all job data: /job/api/job
    url(r'^api/job/$', views.get_job_json, name='job_api'),
    #link response all job waiting data: /job/api/waiting
    url(r'^api/waiting/$', views.get_waiting_json, name='waiting_api'),
    #link response all job running data: /job/api/running
    url(r'^api/running/$', views.get_running_json, name='running_api'),
    #link response all job paused data: /job/api/paused
    url(r'^api/paused/$', views.get_paused_json, name='paused_api'),
    #link response all job completed data: /job/api/completed
    url(r'^api/completed/$', views.get_completed_json, name='completed_api'),
    #link response all job aborted data: /job/api/aborted
    url(r'^api/aborted/$', views.get_aborted_json, name='aborted_api'),
    #link response job pamrams data: /job/api/<job_id>
    url(r'^api/job/(?P<jid>\d+)/$', views.get_job_params, name='jparams'),

    url(r'^api/(?P<wfid>.+)/create/$', views.create_job, name='create_job'),
    url(r'^api/(?P<jid>\d+)/modify/$', views.modify_job, name='modify_job'),
    url(r'^api/(?P<jid>\d+)/delete/$', views.delete_job, name='delete_job'),
    url(r'^api/(?P<jid>\d+)/start/$', views.start_job, name='start_job'),
    url(r'^api/(?P<jid>\d+)/abort/$', views.abort_job, name='abort_job'),

    #link response template show all job data: /job/
    url(r'^$', views.get_job, name='job'),
    #link response template show all job waiting data: /job/waiting
    url(r'^waiting/$', views.get_waiting, name='waiting'),
    #link response template show all job running data: /job/running
    url(r'^running/$', views.get_running, name='running'),
    #link response template show all job paused data: /job/paused
    url(r'^paused/$', views.get_paused, name='paused'),
    #link response template show all job completed data: /job/completed
    url(r'^completed/$', views.get_completed, name='completed'),
    #link response template show all job aborted data: /job/aborted
    url(r'^aborted/$', views.get_aborted, name='aborted'),
    #link api get name and id job
    url(r'^api/job-name/$', views.get_job_name, name='job_name'),
]
