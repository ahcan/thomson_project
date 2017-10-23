from django.conf.urls import url
from . import views


urlpatterns = [

    #==============================
    # URL of accounts
    #==============================
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^password/$', views.password_change, name='password_change'),
]
