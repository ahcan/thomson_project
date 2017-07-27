from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/workflow/$', views.workflow_json, name='workflow_json'),
    url(r'^$', views.get_workflow, name='workflow'),
    url(r'^$', views.test_clock, name='clock'),
]
