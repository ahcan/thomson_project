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
#-------------------------------------ALL JOB--------------------------------#
#                                                                            #
##############################################################################
#Link get all job: /job/api/job
def get_job_json(request):
    job_list = Job().get_job()
    return HttpResponse(job_list, content_type='application/json', status=200)

#Link template show all job: /job/
def get_job(request):
	return render_to_response('job/job.html')

#############################################################################
#                                                                           #
#------------------------------------WAITING--------------------------------#
#                                                                           #
#############################################################################

#Link get all Job Waiting: /job/api/waiting
def get_waiting_json(request):
    waiting_list = Job().get_Waiting()
    return HttpResponse(waiting_list, content_type='application/json', status=200)

#Link get teamplate show jobs waiting: /job/waiting
def get_waiting(request):
	return render_to_response('job/job_waiting.html')

##############################################################################
#                                                                            #
#------------------------------------RUNNING---------------------------------#
#                                                                            #
##############################################################################

#Link gell all Job running: /job/api/running
def get_running_json(request):
    running_list = Job().get_Running()
    return HttpResponse(running_list, content_type='application/json', status=200)

#Link get template show Jobs running: /job/running 
def get_running(request):
	return render_to_response('job/job_running.html')

##############################################################################
#                                                                            #
#-----------------------------------PAUSED-----------------------------------#
#                                                                            #
##############################################################################

#Link get all Job paused: /job/api/paused
def get_paused_json(request):
    paused_list = Job().get_Paused()
    return HttpResponse(paused_list, content_type='application/json', status=200)

#Link template show jobs paused: /job/paused
def get_paused(request):
	return render_to_response('job/job_paused.html')

##############################################################################
#                                                                            #
#----------------------------------COMPLETED---------------------------------#
#                                                                            #
##############################################################################

#Link get all job completed: /job/api/completed
def get_completed_json(request):
    completed_list = Job().get_Completed()
    return HttpResponse(completed_list, content_type='application/json', status=200)

#link template show jobs completed: /job/completed
def get_completed(request):
	return render_to_response('job/job_completed.html')

##############################################################################
#                                                                            #
#-----------------------------------ABORTED----------------------------------#
#                                                                            #
##############################################################################

#Link get all Job aborted: /job/api/aborted
def get_aborted_json(request):
    aborted_list = Job().get_Aborted()
    return HttpResponse(aborted_list, content_type='application/json', status=200)

#Link template show jobs aborted: /job/aborted
def get_aborted(request):
	return render_to_response('job/job_aborted.html')

#######################################################################
#                                                                     #
#------------------------------JOB DETAIL-----------------------------#
#                                                                     #
#######################################################################

#Link get params by job_id
def get_job_params(request, jid):
    param_list = JobDetail('jid').get_param()
    return HttpResponse(param_list, content_type='application/json', status=200)
	