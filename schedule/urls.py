from django.conf.urls import url
from . import views

urlpatterns = [
    #link response all crontab data: /crontabSMP/api/crontabSMP
    url(r'^api/schedule/$', views.get_schedule_json, name='schedule_api'),
    url(r'^add/$', views.get_add, name="add_job"),
    url(r'^delete/(?P<id>[0-9]+)/$',views.remove_schedule, name='delete_schedule'),
    url(r'^$', views.get_index, name="index"), 
]
