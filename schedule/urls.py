from django.conf.urls import url
from . import views

urlpatterns = [
    #link response all crontab data: /crontabSMP/api/crontabSMP
    url(r'^api/schedule/$', views.get_schedule_list_json, name='schedule_api'),
    url(r'^add/$', views.add_schedule, name="add_job"),
    url(r'^delete/(?P<id>[0-9]+)/$',views.remove_schedule, name='delete_schedule'),
    url(r'^detail/(?P<id>[0-9]+)/$',views.redirect_schedule, name='schedule_detail'),
    url(r'^api/schedule/(?P<id>[0-9]+)/$',views.get_schedule_json, name='get_schedule'),
    url(r'^api/history/$',views.get_schedule_history_json, name='get_schedule_history'),
    url(r'^api/history/(?P<id>[0-9]+)/$',views.get_schedule_history_detail_json, name='get_schedule_history_detail'),
    url(r'^$', views.get_index, name="index"),
]
