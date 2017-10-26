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
from accounts.user_info import *
from setting.DateTime import *

# Create your views here.

##############################################################################
#                                                                            #
#-------------------------------------ALL JOB--------------------------------#
#                                                                            #
##############################################################################
#Link get all job: /job/api/job
@require_http_methods(['GET'])
# @csrf_exempt
def get_schedule_list_json(request):
    schedule_list = Crontab().get_all()
    #print schedule_list
    return HttpResponse(schedule_list, content_type='application/json', status=200)
def get_index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response("schedule/schedule.html", user)

@require_http_methods(['GET', 'POST'])
@csrf_exempt
def add_schedule(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    # get value post
    agrs={}
    if request.method=='POST':
        data = None
        list_jobid = ''
        date_time = None
        action = 'start'
        try:
            data = json.loads(request.body)
        except Exception as e:
            agrs["detail"] = "No data input found!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        '''Validate date time YYYY-MM-DD hh:mm:ss'''
        try:
            date_time = data['date_time']
            date_time_pattern = re.compile("\d{4}[/.-]\d{2}[/.-]\d{2} \d{2}:\d{2}:\d{2}")
            date_time = re.findall(date_time_pattern, date_time)
            date_time = date_time[0]
            schedule_datetime = DateTime().conver_human_creadeble_2_unix_timetamp(date_time)
            now = DateTime().get_now() + 60
            if schedule_datetime <= now:
                agrs["detail"] = "Schedule must grater than now 1 minutes!"
                messages = json.dumps(agrs)
                return HttpResponse(messages, content_type='application/json', status=203)
        except Exception as e:
            agrs["detail"] = "Invalid data datetime!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        '''End alidate date time'''
        '''validate jobid input'''
        try:
            jobid_list = data['jobid_list']
            job_pattern = re.compile("\d{3,10}")
            list_job = re.findall(job_pattern,jobid_list)
            for job in list_job:
                list_jobid = list_jobid + job + ','
            ''' trip the last ','''
            if list_jobid:
                list_jobid = list_jobid[:-1]
            else:
                agrs["detail"] = "JobID: %s not found!"%(jobid_list)
                messages = json.dumps(agrs)
                return HttpResponse(messages, content_type='application/json', status=203)
            ''' end trip'''
        except Exception as e:
            agrs["detail"] = "Invalid data JobID!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        '''end validate'''
        '''Create crontab string'''
        schedule = Crontab().create(date_time, list_jobid, action)
        '''install crontab to server'''
        if schedule:
            '''
            Mesages return None is success
            Mesages return string is fail
            '''
            ##check crontab fortmat
            validate_schedule = CrontabDetail(schedule).serialization()
            if not validate_schedule:
            	agrs["detail"] = "Invalid data input JobID or datetime!"
                messages = json.dumps(agrs)
                return HttpResponse(messages, content_type='application/json', status=203)
            ##End check
            '''Write log'''
            
            '''End write log'''
            messages = Crontab().append(validate_schedule)
            if not messages:
                agrs["detail"] = "Successfully added to jobid: %s"%(list_jobid)
                messages = json.dumps(agrs)
                return HttpResponse(messages, content_type='application/json', status=202)
            else:
                agrs["detail"] = messages
                messages = json.dumps(agrs)
                return HttpResponse(messages, content_type='application/json', status=203)
        else:
            agrs["detail"] = schedule
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
    else:
        user = user_info(request)
        return render_to_response("schedule/addJob.html", user)

### remove schedule ###
@require_http_methods(['DELETE'])
@csrf_exempt
def remove_schedule(request, id):
    agrs={}
    if request.method=='DELETE':
        mesages = Crontab().delete(id)
        if not mesages:
            agrs["detail"] = "Successfully remove to jobid: %s"%(id)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)
        else:
            agrs["detail"] = mesages
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
    else:
        return HttpResponse(status=status.HTTP_502_BAD_GATEWAY)

### api time countdown and server ###
@require_http_methods(['GET'])
def get_schedule_json(request, id):
	schedule = CrontabDetail(id).get_schedule()
	return HttpResponse(schedule, content_type='application/json', status=status.HTTP_200_OK)

def redirect_schedule(request, id):
	args={}
	args['id'] = id
	args['email'] = request.user.email if request.user.email else request.user.username
	args['is_superuser'] = 'true' if request.user.is_superuser else 'false'
	args['is_staff'] =  'true' if request.user.is_staff else 'false'
	return render_to_response("schedule/schedule_detail.html",args)
