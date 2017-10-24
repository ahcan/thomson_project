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

# Create your views here.

#######################################################################
#                                                                     #
#------------------------------WORKFLOW-------------------------------#
#                                                                     #
#######################################################################

@require_http_methods(['GET'])
@csrf_exempt
def workflow_json(request):
    workflow_list = Workflow().get_workflow()
    return HttpResponse(workflow_list, content_type='application/json', status=200)

def get_workflow(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response('workflow/workflow.html', user)

#######################################################################
#                                                                     #
#--------------------------WORKFLOW DETAIL----------------------------#
#                                                                     #
#######################################################################

@require_http_methods(['GET'])
@csrf_exempt
def get_workflow_params(request, wfid):
	param_list = WorkflowDetail(wfid).get_param()
	return HttpResponse(param_list, content_type='application/json', status=200)


# @require_http_methods(['POST'])
# @csrf_exempt
