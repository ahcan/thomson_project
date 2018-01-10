from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse 
from rest_framework import status
from setting.get_thomson_api import *
from accounts.user_info import *
from django.contrib.auth.decorators import login_required
from system.utils import DatabaseNode as NodeDB

# Create your views here.

#######################################################################
#                                                                     #
#-------------------------------SYSTEM--------------------------------#
#                                                                     #
#######################################################################

#Main template dashboard /system
def get_system(request, thomson_name):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response('system/'+thomson_name+'.html', user)

#Link get thomson datetime: /system/api/datetime
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

def datetime_json(request, thomson_name):
    date_time = Thomson(thomson_name).get_datetime()
    return HttpResponse(date_time, content_type='application/json', status=200)

#Link get thomson datetime: /system/api/mountpoint
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

def mountpoint_list_json(request, thomson_name):
    mountpoint_list = Thomson(thomson_name).get_mountpoint()
    return HttpResponse(mountpoint_list, content_type='application/json', status=200)

#Link get thomson info CPU, RAAM: /system/api/status
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

def get_system_status_json(request, thomson_name):
    system_status = Thomson(thomson_name).get_system_status()
    return HttpResponse(system_status, content_type='application/json', status=200)

#Link get job status: /system/api/jobstatus
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

def get_job_status_json(request, thomson_name):
    job_status = Thomson(thomson_name).get_job_status()
    return HttpResponse(job_status, content_type='application/json', status=200)

#Link get info CPU, RAM... each node: /system/api/status
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

def get_nodes_status_json(request, thomson_name):
    # nodes_status = Node(thomson_name).get_info()
    nodes_status = NodeDB(thomson_name).get_all_node_json()
    return HttpResponse(nodes_status, content_type='application/json', status=200)

#Link get list job on node: /system/api/<nid>/
@require_http_methods(['GET'])
@csrf_exempt
@login_required()
    
def get_node_job_json(request, node_id, thomson_name):
    nodes_status = NodeDetail(node_id, thomson_name).get_list_job()
    return HttpResponse(nodes_status, content_type='application/json', status=200)

@login_required()
def redirect_node(request, node_id):
    arg={}
    arg['node_id'] = node_id
    return render_to_response('system/system_detail.html',arg)

# link to page monitor
@login_required()
def monitor(request):
    user = user_info(request)
    return render_to_response('system/monitor.html', user)

@login_required()
def test(request):
    user = user_info(request)
    return render_to_response('system/monitor.html', user)    

@login_required()
def get_license_json(request, thomson_name):
    license_status = Thomson(thomson_name).get_license()
    return HttpResponse(license_status, content_type='application/json', status=200)

@require_http_methods(['GET'])
@login_required()
def get_db_node(request, thomson_name):
    nodes =  NodeDB(thomson_name).get_all_node()
    return HttpResponse(nodes, content_type='application/json', status=200)
