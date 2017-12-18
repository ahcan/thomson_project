from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/workflow/$', views.workflow_json, name='workflow_json'),
    url(r'^$', views.get_workflow, name='workflow'),
    url(r'^api/(?P<thomson_name>\w+\-+\w+)/workflow/(?P<wfid>.+)/$', views.get_workflow_params, name='wfparams'),
]
