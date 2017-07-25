from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/job/$', views.job_json, name='job_json'),

    url(r'^$', views.get_job, name='job'),
]
