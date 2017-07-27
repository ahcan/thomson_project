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

def log_list_json(request):
    """
    List all Logs.
    """
    log_list = Log().get_log()
    return HttpResponse(log_list, content_type='application/json', status=200)

def get_log(request):
    return render_to_response('log/log.html')

##############################################################################
#                                                                            #
#---------------------------------CRITICAL LOG-------------------------------#
#                                                                            #
##############################################################################

def open_log_list_json(request):
    """
    List all Logs.
    """
    log_list = Log().get_open()
    return HttpResponse(log_list, content_type='application/json', status=200)

def get_open_log(request):
    return render_to_response('log/log_open.html')

##############################################################################
#                                                                            #
#---------------------------------CRITICAL LOG-------------------------------#
#                                                                            #
##############################################################################

def log_by_jobID_list_json(request, job_id):
    log_list = Log().get_by_jobID(int(job_id))
    return HttpResponse(log_list, content_type='application/json', status=200)

def get_log_by_jobID(request, job_id):
    return render_to_response('log/log_by_jobID.html')
