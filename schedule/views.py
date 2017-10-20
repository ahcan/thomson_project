from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse 
from rest_framework import status
from utils import *
import re

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
def get_index(request):
	return render_to_response("schedule/schedule.html")
@csrf_exempt
def get_add(request):
	if request.method == 'POST':
		# get value post
		date_time = request.POST.get('ipDay', '').strip()
		jobID = request.POST.get('jobID', '').strip()
		##validate jobid input
		job_pattern = re.compile("\d{3,10}")
		list_job = re.findall(job_pattern,jobID)
		# print list_job
		##end validate
		list_jobid = ''
		for job in list_job:
			list_jobid = list_jobid + job + ','
		if list_jobid:
			list_jobid = list_jobid[:-1]
		schedule = Crontab().create(date_time, list_jobid, 'start')
		if schedule:
			Crontab().append(schedule)
			return HttpResponseRedirect('/schedule/')
		return HttpResponseRedirect('/schedule/')
	else:
		return render_to_response("schedule/addJob.html")

@require_http_methods(['POST'])
@csrf_exempt
def remove_schedule(request, id):
	print id
	print request
	if request.method=='POST':
		Crontab().delete(id)
		return HttpResponse(status=status.HTTP_204_NO_CONTENT)
	else:
		return HttpResponse(status=status.HTTP_502_BAD_GATEWAY)