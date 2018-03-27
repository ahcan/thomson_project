# coding: utf-8
import subprocess
import os
import re
import json
from setting.get_thomson_api import *
from setting.DateTime import *
from schedule.models import *
from django.contrib.auth.models import User

class RequestGetParam:
    def __init__(self, Request):
        self.data = json.loads(Request.body)
    def get_action(self):
        return self.data['action']
    def get_job_id(self, thomson_name):
        jobid_list = ''
        error = ''
        try:
            jobid_list_data = self.data['jobid_list']
            # job_pattern = re.compile("\d{3,10}")
            # jobid_list_data = re.findall(job_pattern,jobid_list_data)
            jobid_not_found = ''
            jobid_list_all = Job(thomson_name).get_jobid_list()
            for job in jobid_list_data:
                job = job['jid']
                if int(job) in jobid_list_all:
                    jobid_list = jobid_list + str(job) + ','
                else:
                    jobid_not_found = jobid_not_found + job + ' '
            if jobid_not_found:
                error = "JobID: %s not found!"%(jobid_not_found)
                return jobid_list, error
            ''' trip the last ','''
            if jobid_list:
                jobid_list = jobid_list[:-1]
            else:
                error = "JobID: %s not found!"%(jobid_list_data)
                return jobid_list, error
            return jobid_list, error
            ''' end trip'''
        except Exception as e:
            error = "Invalid data JobID!"
            return jobid_list, error
    def get_date_time(self):
        date_time = ''
        error = ''
        try:
            date_time_data = self.data['date_time']
            date_time_pattern = re.compile("\d{4}[/.-]\d{2}[/.-]\d{2} \d{2}:\d{2}:\d{2}")
            date_time_data = re.findall(date_time_pattern, date_time_data)
            date_time = date_time_data[0]
            schedule_datetime = DateTime().conver_human_creadeble_2_unix_timetamp(date_time)
            now = DateTime().get_now() + 60
            if schedule_datetime <= now:
                error = "Schedule must grater than now 1 minutes!"
                return date_time, error
            return date_time, error 
        except Exception as e:
            error = "Invalid data datetime!"
            return date_time, error
    def get_description(self):
        return 'kakaka'

class Crontab:

    def create(self, date_time, jobid, action, schedule_id):
        if not date_time.isdigit():
            try:
                date_time = DateTime().conver_human_creadeble_2_unix_timetamp(date_time)
            except Exception as e:
                return None
        dt=datetime.fromtimestamp(date_time)
        #print dt
        DD = dt.day
        MM = dt.month
        hh = dt.hour
        #print hh
        mm = dt.minute
        ss = dt.second
        dayofweek = dt.isocalendar()[2]
        task = """%s %s %s %s %s sleep %s; /bin/python /script/crontabSMP/job.py -j %s -s %s -n %s"""%(mm,hh,DD,MM,dayofweek,ss,jobid,action,str(schedule_id))
        return task

    def _runcmd(self, cmd, input=None):
        if input is not None:
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 close_fds=True, preexec_fn=os.setsid)
        else:
            p = subprocess.Popen(cmd, shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 close_fds=True, preexec_fn=os.setsid)

        stdoutdata, stderrdata = p.communicate(input)
        return p.returncode, stderrdata, stdoutdata

    # currently installed crontabs
    def get_list(self):
        retcode, err, installed_content = self._runcmd('crontab -l')
        if retcode != 0 and 'no crontab for' not in err:
            raise OSError('crontab not supported in your system')
        else:
            # merge the new crontab with the old one
            installed_content = installed_content.rstrip("\n")
            return installed_content
    '''
    return None is success
    return string is fail
    '''
    def append(self, content='', override=False):
        if not content:
            return 'Crontab must be specified'
        if override:
            installed_content = ''
        else:
            installed_content =  self.get_list()
            #print installed_content
        installed_crontabs = installed_content.split('\n')
        for crontab in content.split('\n'):
            if crontab and crontab not in installed_crontabs:
                if not installed_content:
                    installed_content += crontab
                else:
                    installed_content += '\n%s' % crontab
            else:
                return 'New crontab is available'
        if installed_content:
            installed_content += '\n'
        # install back
        retcode, err, out = self._runcmd('crontab', installed_content)
        if retcode != 0: 
            return 'failed to install crontab, check if crontab is valid'
        else:
            return None

    '''
    return None is success
    return string is fail
    '''
    def delete(self, id = None):
        if not id:
            return 'ID must be specified'
        else:
            id = int(id)
        installed_content =  self.get_list()
        if not installed_content:
            return 'Schedule is empty!'
        #remove schedule by line number
        new_content = ''
        for task in installed_content.split('\n'):
            schedule = CrontabDetail(task).serialization()
            if schedule:
                schedule_id = int(re.search('(?<=-n )\d+',schedule).group(0))
                if id == schedule_id:
                    continue
                else:
                    new_content += schedule + '\n'
            else:
                new_content += task + '\n'

        #end remove        
        # install back and return status
        if new_content:
            retcode, err, out = self._runcmd('crontab', new_content)
            if retcode != 0: 
                return 'Failed to remove crontab, check if crontab is valid'
            else:
                return None
        else:
            os.system('crontab -r')
            return None

    def get_cron_by_id(self, id = None):
        if not id:
            raise ValueError('neither id must be specified')
        else:
            id = int(id)
        installed_content =  self.get_list()
        if not installed_content:
            return None
        #find schedule by line number
        task = ''
        for schedule in installed_content.split('\n'):
            schedule = CrontabDetail(schedule).serialization()
            if schedule:
                schedule_id = int(re.search('(?<=-n )\d+',schedule).group(0))
                if schedule_id == id:
                    task = schedule

        #end remove        
        # find back and return status
        return task

    def get_all(self, thomson_name):
        list_task = self.get_list()
        agrs = []
        for task in list_task.split('\n'):
            schedule = CrontabDetail(task).serialization()
            if schedule:
                schedule_id,ss,mm,hh,DD,MM,YYYY,dayofweek,list_jid,action,full_date,state,alarm = CrontabDetail(schedule).get_pattern()
                #print list_jid
                array_jid = []
                for jid in list_jid:
                    array_jid.append(int(jid))
                list_job = Job(thomson_name).get_job_detail_by_job_id(array_jid)
                agrs.append({'id'              : int(schedule_id),
                             'list_job'        : list_job,
                             'action'          : action,
                             'unix_timestamp'  : full_date,
                             'state'           : int(state),
                             'alarm'           : alarm
                            })
        return json.dumps(agrs)

    
class CrontabDetail:
    def __init__(self, task):
        if not task.isdigit():
            self.task = task
        else:
            self.task = Crontab().get_cron_by_id(task)
    def serialization(self):
        cron_pattern=re.compile("[ ?\d{1,2}]*\ sleep \d{1,2}; /bin/python /script/crontabSMP/job.py -[Jj] [,?\d{3,10}]*\ -[Ss] (?:[Ss]tart|[Ss]top) -n \d+")
        #cron_pattern=re.compile("\d{1,2}\ \d{1,2}\ \d{1,2}\ \d{1,2}\ \d{1,2}\ sleep \d{1,2}; /bin/python /script/crontabSMP/job.py -[Jj] \d{3,10}\ -[Ss] (?:[Ss]tart|[Ss]top)")
        cron = re.findall(cron_pattern, self.task)
        if cron:
            return cron[0]
        else:
            return None
    def get_waiting_time(self, schedule_time):
        now = DateTime().get_now()
        minus_dt = schedule_time - now
        if minus_dt > 0:
            mm, ss = divmod(minus_dt, 60)
            hh, mm = divmod(mm, 60)
            DD, hh = divmod(hh, 24)
            waiting_time = "%d day(s) %02d:%02d:%02d" % (DD, hh, mm, ss)
            return waiting_time
        return None

#state = 1: schedule complete
#state = 0: schedule waiting
    def get_pattern(self):
        cron = self.serialization()
        if not cron:
            return None
        schedule_id = int(re.search('(?<=-n )\d+',cron).group(0))
        number_pattern=re.compile("\d{1,2}")
        list_time=re.findall(number_pattern, cron)
        ss = list_time[5]
        mm = list_time[0]
        hh = list_time[1]
        DD = list_time[2]
        MM = list_time[3]
        #  nam lich
        YYYY = DateTime().get_year()
        dayofweek = list_time[4]
        full_date = 0
        action = None
        alarm = ''
        state = 1
        jid_pattern = re.compile("\d{3,10}")    
        list_jid = re.findall(jid_pattern, cron)
        action = re.search('(?<=-s )\w+',cron).group(0)
        full_date = DateTime().convert_date_pattern_2_unix_timestamp(ss,mm,hh,DD,MM,YYYY)
        alarm = self.get_waiting_time(full_date)
        if alarm:
            state = 0
        return schedule_id,ss,mm,hh,DD,MM,YYYY,dayofweek,list_jid,action,full_date,state,alarm
    #parse crontab to human readable fortmat
    def human_readable(self):
        message = ''
        schedule_id,ss,mm,hh,DD,MM,YYYY,dayofweek,list_jid,action,full_date,state,alarm = self.get_pattern()
        human_date = "%s-%s-%s %s:%s:%s"%(YYYY,MM,DD,hh,mm,ss)
        message = 'At %s %s job(s) ID: %s.'%(human_date, action, list_jid)
        return message

    def get_schedule(self, thomson_name):
        agrs = []
        schedule = CrontabDetail(self.task).serialization()
        if schedule:
            schedule_id,ss,mm,hh,DD,MM,YYYY,dayofweek,list_jid,action,full_date,state,alarm = self.get_pattern()
            array_jid = []
            for jid in list_jid:
                array_jid.append(int(jid))
            list_job = Job(thomson_name).get_job_detail_by_job_id(array_jid)
            now = DateTime().get_now()
            agrs.append({'list_job'        : list_job,
                         'action'          : action,
                         'schedule_date'   : full_date,
                         'svr_date'        : int(now),
                         'state'           : int(state),
                         'message'         : self.human_readable()
                        })
        return json.dumps(agrs)


class ScheduleHistory:
    def create_message(self, user_name='', action = '', crontab = ''):
        host = settings.THOMSON_HOST['thomson-hcm']['host']
        message = ''
        msg = CrontabDetail(crontab).human_readable()
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        message = 'User %s %s schedule content(%s) in host %s at %s.'%(user_name, action, msg, host, now)
        return message

    def write_history(self, user_name, action, schedule_id):
        schedule = Crontab().get_cron_by_id(schedule_id)
        schedule_obj = Schedule.objects.get(id=int(schedule_id))
        msg = self.create_message(user_name, action, schedule)
        now = DateTime().get_now()
        new_history = History(schedule=schedule_obj, date_time=now, host=settings.THOMSON_HOST['thomson-hcm']['host'], messages=msg)
        new_history.save()
        return 1

    def get_new_id(self, request):
        host = settings.THOMSON_HOST['thomson-hcm']['host']
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        action = RequestGetParam(request).get_action()
        jobid_list, error = RequestGetParam(request).get_job_id('thomson-hcm')
        schedule_time, error = RequestGetParam(request).get_date_time()
        description = RequestGetParam(request).get_description()
        schedule_time = DateTime().conver_human_creadeble_2_unix_timetamp(schedule_time)
        now = DateTime().get_now()
        new_schedule = Schedule(user=user, create_time=now, schedule_time=schedule_time, action=action, host=host, description=description)
        new_schedule.save()
        n = Schedule.objects.get(create_time=now)
        return n.id
