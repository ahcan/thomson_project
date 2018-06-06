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

# Create your views here.

##############################################################################
#                                                                            #
#--------------------------------------ALL LOG-------------------------------#
#                                                                            #
##############################################################################
@require_http_methods(['GET'])
@csrf_exempt
@login_required()
def get_logs(request, thomson_name):
    """
    List all Logs.
    /log/api/log
    """
    if not request.user.is_authenticated():
        return HttpResponse(status = 401)
    log_list = Log(thomson_name).get_log()
    return HttpResponse(log_list, content_type='application/json', status=200)

def get_log(request, thomson_name):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    """
    Template show list all Logs.
    /log/
    """
    return render_to_response('log/'+thomson_name+'.html',user)

##############################################################################
#                                                                            #
#----------------------------GET ALL LOG BY SEVERITY-------------------------#
#                                                                            #
##############################################################################
@require_http_methods(['POST'])
@csrf_exempt
def filter_log(requests, thomson_name):
    if not requests.user.is_authenticated():
        return HttpResponse(status = 401)
    args = {}
    data =''
    try:
        data = json.loads(requests.body)
    except Exception as e:
        args['detail'] = "No data input found!"
        message = json.dumps(args)
        return HttpResponse(message, content_type='application/json', status=203)
    log_list = Log(thomson_name).get_by_sevJob(data['sev'])
    return HttpResponse(log_list, content_type='application/json', status = 200)

##############################################################################
#                                                                            #
#-----------------------------------OPEN LOG---------------------------------#
#                                                                            #
##############################################################################
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response('log/log_open.html',user)

##############################################################################
#                                                                            #
#-------------------------------GET LOG BY JOBID-----------------------------#
#                                                                            #
##############################################################################
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

def get_log_by_jobID_list_json(requests, job_id, thomson_name):
    """
    List all Logs by Job_ID.
    /log/api/thomosn_name/<Job_ID>/
    """
    if not requests.user.is_authenticated():
        return HttpResponse(status = 401)
    try:
        log_list = Log(thomson_name).get_by_jobID(int(job_id))
        return HttpResponse(log_list, content_type='application/json', status=200)
    except Exception as e:
        return HttpResponse(status = 501)

##############################################################################
#                                                                            #
#---------------------------------SYSTEM LOG---------------------------------#
#                                                                            #
##############################################################################
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

def get_system_log_list_json(request):
    """
    Template show list all system Logs.
    /log/api/system
    """
    log_list = Log(thomson_name).get_sys_log()
    return HttpResponse(log_list, content_type='application/json', status=200)

def get_system_log(request):
    """
    Template show list all system Logs.
    /log/api/system
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response('log/log_system.html',user)

@require_http_methods(['GET'])
# @require_http_methods(['POST'])
def test_captcha(request):
    return render_to_response('log/testcaptcha.html')

@require_http_methods(['POST'])
@csrf_exempt
def get_captcha(request):
    print'#############'
    print str(request.body)
    return HttpResponse('sdfsdfds', status=200)
    
