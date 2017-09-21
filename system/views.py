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

#Main template dashboard /system
def get_system(request):
	return render_to_response('system/system.html')

#Link get thomson datetime: /system/api/datetime
@require_http_methods(['GET'])
@csrf_exempt
def datetime_json(request):
    date_time = Thomson().get_datetime()
    return HttpResponse(date_time, content_type='application/json', status=200)

#Link get thomson datetime: /system/api/mountpoint
@require_http_methods(['GET'])
@csrf_exempt
def mountpoint_list_json(request):
    mountpoint_list = Thomson().get_mountpoint()
    return HttpResponse(mountpoint_list, content_type='application/json', status=200)

#Link get thomson info CPU, RAAM: /system/api/status
@require_http_methods(['GET'])
@csrf_exempt
def get_system_status_json(request):
    system_status = Thomson().get_system_status()
    return HttpResponse(system_status, content_type='application/json', status=200)

#Link get job status: /system/api/jobstatus
@require_http_methods(['GET'])
@csrf_exempt
def get_job_status_json(request):
    job_status = Thomson().get_job_status()
    return HttpResponse(job_status, content_type='application/json', status=200)

#Link get info CPU, RAM... each node: /system/api/status
@require_http_methods(['GET'])
@csrf_exempt
def get_nodes_status_json(request):
    nodes_status = Thomson().get_nodes_status()
    return HttpResponse(nodes_status, content_type='application/json', status=200)
