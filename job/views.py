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
    date_time = Job().get_job()
    return HttpResponse(date_time, content_type='application/json', status=200)

def get_job(request):
	return render_to_response('job/job.html')

#############################################################################
#                                                                           #
#------------------------------------WAITING--------------------------------#
#                                                                           #
#############################################################################

def waiting_job_json(request):
    date_time = Job().get_Waiting()
    return HttpResponse(date_time, content_type='application/json', status=200)

def get_waiting_job(request):
	return render_to_response('job/job_waiting.html')

##############################################################################
#                                                                            #
#------------------------------------RUNNING---------------------------------#
#                                                                            #
##############################################################################

def running_job_json(request):
    date_time = Job().get_Running()
    return HttpResponse(date_time, content_type='application/json', status=200)

def get_running_job(request):
	return render_to_response('job/job_running.html')

##############################################################################
#                                                                            #
#-----------------------------------PAUSED-----------------------------------#
#                                                                            #
##############################################################################

def paused_job_json(request):
    date_time = Job().get_Paused()
    return HttpResponse(date_time, content_type='application/json', status=200)

def get_paused_job(request):
	return render_to_response('job/job_paused.html')

##############################################################################
#                                                                            #
#----------------------------------COMPLETED---------------------------------#
#                                                                            #
##############################################################################

def completed_job_json(request):
    date_time = Job().get_Completed()
    return HttpResponse(date_time, content_type='application/json', status=200)

def get_completed_job(request):
	return render_to_response('job/job_completed.html')

##############################################################################
#                                                                            #
#-----------------------------------ABORTED----------------------------------#
#                                                                            #
##############################################################################

def aborted_job_json(request):
    date_time = Job().get_Aborted()
    return HttpResponse(date_time, content_type='application/json', status=200)

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

	