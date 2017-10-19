from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse 
from rest_framework import status
from utils import *

# Create your views here.

##############################################################################
#                                                                            #
#-------------------------------------ALL JOB--------------------------------#
#                                                                            #
##############################################################################
#Link get all job: /job/api/job
@require_http_methods(['GET'])
# @csrf_exempt
def get_schedule_json(request):
    schedule_list = Crontab().get_all()
    print schedule_list
    return HttpResponse(schedule_list, content_type='application/json', status=200)
@csrf_exempt
def get_add(request):
	if request.method == 'POST':
		# get value post
		date = request.POST.get('ipDay', '').strip()
		jobID = request.POST.get('jobID', '').strip()
		print date
		print jobID
		return render_to_response("schedule/addJob.html")
		# return HttpResponse(date)
		# return render_to_response("schedule/index.html")
	else:
		return render_to_response("schedule/addJob.html")
