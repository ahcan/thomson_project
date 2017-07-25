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
#------------------------------WORKFLOW-------------------------------#
#                                                                     #
#######################################################################
def workflow_json(request):
    date_time = Workflow().get_workflow()
    return HttpResponse(date_time, content_type='application/json', status=200)

def get_workflow(request):
	return render_to_response('workflow/workflow.html')

def workflow_by_jobID_json(request, jobID):
    mountpoint_list = Thomson().get_mountpoint()
    return HttpResponse(mountpoint_list, content_type='application/json', status=200)

def get_workflow_by_jobID(request, jobID):
 	return render_to_response('workflow/job/workflow_by_job.html')
