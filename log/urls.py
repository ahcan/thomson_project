from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/log$', views.log_list_json, name='log_json'),
    url(r'^$', views.get_log, name='log'),
]
