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
def job_json(request):
    job_list = Job().get_job()
    return HttpResponse(job_list, content_type='application/json', status=200)

def get_job(request):
	return render_to_response('job/job.html')

#############################################################################
#                                                                           #
#------------------------------------WAITING--------------------------------#
#                                                                           #
#############################################################################

def waiting_job_json(request):
    waiting_job_list = Job().get_Waiting()
    return HttpResponse(waiting_job_list, content_type='application/json', status=200)

def get_waiting_job(request):
	return render_to_response('job/job_waiting.html')

##############################################################################
#                                                                            #
#------------------------------------RUNNING---------------------------------#
#                                                                            #
##############################################################################

def running_job_json(request):
    running_job_list = Job().get_Running()
    return HttpResponse(running_job_list, content_type='application/json', status=200)

def get_running_job(request):
	return render_to_response('job/job_running.html')

##############################################################################
#                                                                            #
#-----------------------------------PAUSED-----------------------------------#
#                                                                            #
##############################################################################

def paused_job_json(request):
    paused_job_list = Job().get_Paused()
    return HttpResponse(paused_job_list, content_type='application/json', status=200)

def get_paused_job(request):
	return render_to_response('job/job_paused.html')

##############################################################################
#                                                                            #
#----------------------------------COMPLETED---------------------------------#
#                                                                            #
##############################################################################

def completed_job_json(request):
    completed_job_list = Job().get_Completed()
    return HttpResponse(completed_job_list, content_type='application/json', status=200)

def get_completed_job(request):
	return render_to_response('job/job_completed.html')

##############################################################################
#                                                                            #
#-----------------------------------ABORTED----------------------------------#
#                                                                            #
##############################################################################

def aborted_job_json(request):
    aborted_job_list = Job().get_Aborted()
    return HttpResponse(aborted_job_list, content_type='application/json', status=200)

def get_aborted_job(request):
	return render_to_response('job/job_aborted.html')

#######################################################################
#                                                                     #
#------------------------------JOB DETAIL-----------------------------#
#                                                                     #
#######################################################################

def get_job_params(request, jid):
    param_list = JobDetail('jid').get_param()
    return HttpResponse(param_list, content_type='application/json', status=200)

	