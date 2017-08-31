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

##############################################################################
#                                                                            #
#--------------------------------------ALL LOG-------------------------------#
#                                                                            #
##############################################################################
@require_http_methods(['GET'])
@csrf_exempt
def get_log_list_json(request):
    """
    List all Logs.
    /log/api/log
    """
    log_list = Log().get_log()
    return HttpResponse(log_list, content_type='application/json', status=200)

def get_log(request):
    """
    Template show list all Logs.
    /log/
    """
    return render_to_response('log/log.html')

##############################################################################
#                                                                            #
#-----------------------------------OPEN LOG---------------------------------#
#                                                                            #
##############################################################################
@require_http_methods(['GET'])
@csrf_exempt
def get_open_log_list_json(request):
    """
    List all open Logs.
    /log/api/open/
    """
    log_list = Log().get_open()
    return HttpResponse(log_list, content_type='application/json', status=200)

def get_open_log(request):
    """
    Template show list all open Logs.
    /log/open/
    """
    return render_to_response('log/log_open.html')

##############################################################################
#                                                                            #
#-------------------------------GET LOG BY JOBID-----------------------------#
#                                                                            #
##############################################################################
@require_http_methods(['GET'])
@csrf_exempt
def get_log_by_jobID_list_json(request, job_id):
    """
    List all Logs by Job_ID.
    /log/api/<Job_ID>/
    """
    log_list = Log().get_by_jobID(int(job_id))
    return HttpResponse(log_list, content_type='application/json', status=200)

##############################################################################
#                                                                            #
#---------------------------------SYSTEM LOG---------------------------------#
#                                                                            #
##############################################################################
@require_http_methods(['GET'])
@csrf_exempt
def get_system_log_list_json(request):
    """
    Template show list all system Logs.
    /log/api/system
    """
    log_list = Log().get_sys_log()
    return HttpResponse(log_list, content_type='application/json', status=200)

def get_system_log(request):
    """
    Template show list all system Logs.
    /log/api/system
    """
    return render_to_response('log/log_system.html')
