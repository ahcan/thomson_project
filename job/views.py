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
from utils import DatabaseJob as JobDB

# Create your views here.

##############################################################################
#                                                                            #
#-------------------------------------ALL JOB--------------------------------#
#                                                                            #
##############################################################################
#Link get all job: /job/api/job
@require_http_methods(['GET'])
@csrf_exempt
@login_required()
def get_job_json(request, thomson_name):
    job_list = JobDB().json_job_host(thomson_name)
    # job_list = Job().get_job()
    return HttpResponse(job_list, content_type='application/json', status=200)

#link get all job name and id /job/api/job-name
@login_required()
def get_job_name(request, thomson_name):
    job_list = JobDB().json_job_name(thomson_name)
    return HttpResponse(job_list, content_type='application/json', status=200)

#Link template show all job: /job/
@login_required()
def get_job(request, thomson_name):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response('job/'+thomson_name+'.html', user)

@require_http_methods(['GET'])
@login_required()
def count_job_by_host(request, thomson_name):
    jobs = JobDB().count_job_host(thomson_name)
    return HttpResponse(jobs, content_type='application/json', status=200)
#############################################################################
#                                                                           #
#------------------------------------WAITING--------------------------------#
#                                                                           #
#############################################################################

#Link get all Job Waiting: /job/api/waiting
@require_http_methods(['GET'])
@csrf_exempt
@login_required()
def get_waiting_json(request):
    waiting_list = Job().get_Waiting()
    return HttpResponse(waiting_list, content_type='application/json', status=200)

#Link get teamplate show jobs waiting: /job/waiting
def get_waiting(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response('job/job_waiting.html', user)

##############################################################################
#                                                                            #
#------------------------------------RUNNING---------------------------------#
#                                                                            #
##############################################################################

#Link gell all Job running: /job/api/running
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

def get_running_json(request):
    running_list = Job().get_Running()
    return HttpResponse(running_list, content_type='application/json', status=200)

#Link get template show Jobs running: /job/running 
def get_running(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response('job/job_running.html', user)

##############################################################################
#                                                                            #
#-----------------------------------PAUSED-----------------------------------#
#                                                                            #
##############################################################################

#Link get all Job paused: /job/api/paused
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

def get_paused_json(request):
    paused_list = Job().get_Paused()
    return HttpResponse(paused_list, content_type='application/json', status=200)

#Link template show jobs paused: /job/paused
def get_paused(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response('job/job_paused.html', user)

##############################################################################
#                                                                            #
#----------------------------------COMPLETED---------------------------------#
#                                                                            #
##############################################################################

#Link get all job completed: /job/api/completed
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

def get_completed_json(request):
    completed_list = Job().get_Completed()
    return HttpResponse(completed_list, content_type='application/json', status=200)

#link template show jobs completed: /job/completed
def get_completed(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response('job/job_completed.html', user)

##############################################################################
#                                                                            #
#-----------------------------------ABORTED----------------------------------#
#                                                                            #
##############################################################################

#Link get all Job aborted: /job/api/aborted
@require_http_methods(['GET'])
@csrf_exempt
@login_required()

def get_aborted_json(request):
    aborted_list = Job().get_Aborted()
    return HttpResponse(aborted_list, content_type='application/json', status=200)

#Link template show jobs aborted: /job/aborted
def get_aborted(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response('job/job_aborted.html', user)

##############################################################################
#                                                                            #
#----------------------------------JOB DETAIL--------------------------------#
#                                                                            #
##############################################################################

#Link get params by job_id
@require_http_methods(['GET'])
@csrf_exempt
@login_required()
def get_job_params(request, jid, thomson_name):
    param_list = JobDetail(jid, thomson_name).get_param()
    return HttpResponse(param_list, content_type='application/json', status=200)

##############################################################################
#                                                                            #
#--------------------------------CREATE NEW JOB------------------------------#
#                                                                            #
##############################################################################

"""curl -H "Content-Type: application/json" -X POST -d 
'{"usernamOST":"xyz","password":"xyz"}'
 http://localhost:8000/job/api/danang/create/
 link: /job/api/create/"""
@require_http_methods(['POST'])
@csrf_exempt
@login_required()
def create_job(request, wfid, thomson_name):
    print wfid
    json_data = json.loads(request.body)
    print json_data
    return HttpResponse(content_type='application/json', status=200)

##############################################################################
#                                                                            #
#----------------------------------UPDATE JOB--------------------------------#
#                                                                            #
##############################################################################

"""curl -H "Content-Type: application/json" -X PUT -d 
'{"username":"xyz","password":"xyz"}'
 http://localhost:8000/job/api/125/modify/
 link: /job/api/<jid>/modify/"""
@require_http_methods(['PUT'])
@csrf_exempt
@login_required()
def modify_job(request, jid):
    print "ok"
    json_data = json.loads(request.body)
    print json_data
    return HttpResponse(json_data, content_type='application/json', status=200)
	
##############################################################################
#                                                                            #
#----------------------------------DELETE JOB--------------------------------#
#                                                                            #
##############################################################################

"""curl -H "Content-Type: application/json" -X DELETE http://localhost:8000/
job/api/125/delete/"""
@csrf_exempt
@login_required()
def delete_job(request, jid):
    if request.method == 'DELETE':
        print "ok"
        return HttpResponse(content_type='application/json', status=200)

##############################################################################
#                                                                            #
#-----------------------------------START JOB--------------------------------#
#                                                                            #
##############################################################################

"""curl -H "Content-Type: application/json" -X PUT http://localhost:8000/
job/api/125/start/
 link: job/api/<jid>/start/"""
@require_http_methods(['PUT'])
@csrf_exempt
@login_required()
def start_job(request, jid, thomson_name):
    result = JobDetail(jid, thomson_name).start()
    arg = {}
    arg["message"] = result
    message = json.dumps(arg)
    print "start"
    return HttpResponse(message, content_type="application.json",status=202)

##############################################################################
#                                                                            #
#----------------------------------RESTART JOB-------------------------------#
#                                                                            #
##############################################################################

"""curl -H "Content-Type: application/json" -X PUT http://localhost:8000/
job/api/125/start/
 link: job/api/<jid>/start/"""
@require_http_methods(['PUT'])
@csrf_exempt
@login_required()
def restart_job(request, jid, thomson_name):
    result = JobDetail(jid, thomson_name).restart(request.user.username)
    arg = {}
    arg["message"] = result
    message = json.dumps(arg)
    print "restart"
    return HttpResponse(message, content_type="application.json",status=202)

##############################################################################
#                                                                            #
#-----------------------------------ABORT JOB--------------------------------#
#                                                                            #
##############################################################################

"""curl -H "Content-Type: application/json" -X PUT http://localhost:8000/
job/api/125/abort/
 link: job/api/<jid>/abort/"""
@require_http_methods(['PUT'])
@csrf_exempt
@login_required()
def abort_job(request, jid, thomson_name):
    result = JobDetail(jid, thomson_name).abort(request.user.username)
    arg = {}
    if result =='OK':
        result = "Job"+jid+" on "+thomson_name+" just be stoped"
    elif request =='NotOK':
        result = "Job"+jid+" on "+thomson_name+" cant not stop"
    arg["message"] = result
    message = json.dumps(arg)
    print "stop"
    return HttpResponse(message, content_type="application.json", status=202)

# Check backup Job
# link job/api/thomson_name/jid/check-backup/
@require_http_methods(['GET'])
@csrf_exempt
@login_required()
def check_bckJob(request, jid, thomson_name):
    lstparam = json.loads(JobDetail(jid, thomson_name).get_param())
    lstparam = lstparam[0]['params']
    for param in lstparam:
        print param
        if param['name'] == 'Define backup input':
            backup = param['value']
        if param['name'] == 'Backup input IP address':
            ip = param['value']
    result = json.dumps([{'backup': backup, 'ip': ip}])
    return HttpResponse(result, content_type="application.json", status=202)
    