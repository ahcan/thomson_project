from django.conf.urls import url
from . import views

urlpatterns = [
    #link response all crontab data: /crontabSMP/api/crontabSMP
    url(r'^api/schedule/$', views.get_schedule_json, name='schedule_api'),
]
