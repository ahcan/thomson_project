from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse 
from rest_framework import status
from setting.get_thomson_api import *

# Create your views here.

#######################################################################
#                                                                     #
#-------------------------------SYSTEM--------------------------------#
#                                                                     #
#######################################################################
def datetime_json(request):
    date_time = Thomson().get_datetime()
    return HttpResponse(date_time, content_type='application/json', status=200)

def get_datetime(request):
	return render_to_response('workflow/workflow.html')

def mountpoint_list_json(request):
    mountpoint_list = Thomson().get_mountpoint()
    return HttpResponse(mountpoint_list, content_type='application/json', status=200)

def get_mountpoint(request):
 	return render_to_response('workflow/workflow.html')

