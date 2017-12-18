from django.conf.urls import url
from . import views

urlpatterns = [
    #link response all job data: /job/api/job
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/job/$', views.get_job_json, name='job_api'),
    #link response job pamrams data: /job/api/<job_id>
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/job/(?P<jid>\d+)/$', views.get_job_params, name='jparams'),

    url(r'^api/(?P<wfid>.+)/create/$', views.create_job, name='create_job'),
    url(r'^api/(?P<jid>\d+)/modify/$', views.modify_job, name='modify_job'),
    url(r'^api/(?P<jid>\d+)/delete/$', views.delete_job, name='delete_job'),
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/(?P<jid>\d+)/start/$', views.start_job, name='start_job'),
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/(?P<jid>\d+)/abort/$', views.abort_job, name='abort_job'),

    #link response template show all job data: /job/
    url(r'^$', views.get_job, name='job'),
    #link api get name and id job
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/job-name/$', views.get_job_name, name='job_name'),
]
