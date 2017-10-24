# coding: utf-8
import subprocess
import os
import re
import json
from setting.get_thomson_api import *
from setting.DateTime import *
class Crontab:

    def create(self, date_time, jobid, action):
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
        task = """%s %s %s %s %s sleep %s; /bin/python /script/crontabSMP/job.py -j %s -s %s"""%(mm,hh,DD,MM,dayofweek,ss,jobid,action )
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

    def append(self, content='', override=False):
        if not content:
            raise ValueError('neither filename or crontab must be specified')
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
                print 'New crontab was available'
        if installed_content:
            installed_content += '\n'
        # install back
        retcode, err, out = self._runcmd('crontab', installed_content)
        if retcode != 0: 
            raise ValueError('failed to install crontab, check if crontab is valid')

    def delete(self, id = None):
        if not id:
            raise ValueError('neither id must be specified')
        else:
            id = int(id)
        installed_content =  self.get_list()
        if not installed_content:
            return 0
        #remove schedule by line number
        new_content = ''
        count = 1
        for schedule in installed_content.split('\n'):
            if count != id:
                #exeption crontab is none
                if schedule:
                    new_content += '%s\n' % schedule
            count +=1
        #end remove        
        # install back and return status
        if new_content:
            retcode, err, out = self._runcmd('crontab', new_content)
            if retcode != 0: 
                raise ValueError('failed to install crontab, check if crontab is valid')
            else:
                return 1
        else:
            os.system('crontab -r')
            return 1

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
        count = 1
        for schedule in installed_content.split('\n'):
            if count == id:
                task = schedule
            count +=1
        #end remove        
        # find back and return status
        return task

    def get_all(self):
        list_task = self.get_list()
        id = 0
        agrs = []
        for task in list_task.split('\n'):
            id+=1
            schedule = CrontabDetail(task).serialization()
            if schedule:
                ss,mm,hh,DD,MM,YYYY,dayofweek,list_jid,action,full_date,state,alarm = CrontabDetail(schedule).get_pattern()
                #print list_jid
                array_jid = []
                for jid in list_jid:
                    array_jid.append(int(jid))
                list_job = Job().get_job_detail_by_job_id(array_jid)
                agrs.append({'id'              : int(id),
                             'ss'              : int(ss),
                             'mm'              : int(mm),
                             'hh'              : int(hh),
                             'DD'              : int(DD),
                             'MM'              : int(MM),
                             'YYYY'            : int(YYYY),
                             'dayofweek'       : int(dayofweek),
                             'list_job'      : list_job,
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
        cron_pattern=re.compile("[ ?\d{1,2}]*\ sleep \d{1,2}; /bin/python /script/crontabSMP/job.py -[Jj] [,?\d{3,10}]*\ -[Ss] (?:[Ss]tart|[Ss]top)")
        #cron_pattern=re.compile("\d{1,2}\ \d{1,2}\ \d{1,2}\ \d{1,2}\ \d{1,2}\ sleep \d{1,2}; /bin/python /script/crontabSMP/job.py -[Jj] \d{3,10}\ -[Ss] (?:[Ss]tart|[Ss]top)")
        cron = re.findall(cron_pattern, self.task)
        if cron:
            return cron[0]
        else:
            return None

#state = 1: schedule complete
#state = 0: schedule waiting

    def get_pattern(self):
        cron = self.serialization()
        if not cron:
            return None
        number_pattern=re.compile("\d{1,2}")
        list_time=re.findall(number_pattern, cron)
        ss = list_time[5]
        mm = list_time[0]
        hh = list_time[1]
        DD = list_time[2]
        MM = list_time[3]
        YYYY = '2017'
        dayofweek = list_time[4]
        full_date = 0
        action = None
        alarm = ''
        state = 1
        jid_pattern = re.compile("\d{3,10}")    
        list_jid = re.findall(jid_pattern, cron)
        reaction_pattern = re.compile("(?:-[Ss] [Ss]tart|-[Ss] [Ss]top)")
        action_pattern = re.compile("([Ss]tart|[Ss]top)")
        reaction = re.findall(reaction_pattern, cron)
        if reaction:
            action = re.findall(action_pattern, reaction[0])
            action = action[0]
        full_date = DateTime().convert_date_pattern_2_unix_timestamp(ss,mm,hh,DD,MM,YYYY)
        now = DateTime().get_now()
        minus_dt = full_date - now
        if minus_dt > 0:
            mm, ss = divmod(minus_dt, 60)
            hh, mm = divmod(mm, 60)
            DD, hh = divmod(hh, 24)
            alarm = "%d day(s) %02d:%02d:%02d" % (DD, hh, mm, ss)
            state = 0
        return ss,mm,hh,DD,MM,YYYY,dayofweek,list_jid,action,full_date,state,alarm
    #parse crontab to human readable fortmat
    def human_readable(self):
        message = ''
        ss,mm,hh,DD,MM,YYYY,dayofweek,list_jid,action,full_date,state,alarm = self.get_pattern()
        human_date = "%s-%s-%s %s:%s:%s"%(YYYY,MM,DD,hh,mm,ss)
        message = 'At %s %s job(s) ID: %s.'%(human_date, action, list_jid)
        return message

    def get_schedule(self):
        agrs = []
        schedule = CrontabDetail(self.task).serialization()
        if schedule:
            ss,mm,hh,DD,MM,YYYY,dayofweek,list_jid,action,full_date,state,alarm = self.get_pattern()
            array_jid = []
            for jid in list_jid:
                array_jid.append(int(jid))
            list_job = Job().get_job_detail_by_job_id(array_jid)
            now = DateTime().get_now()
            agrs.append({'list_job'        : list_job,
                         'action'          : action,
                         'schedule_date'   : full_date,
                         'svr_date'        : int(now),
                         'state'           : int(state),
                         'message'         : self.human_readable()
                        })
        return json.dumps(agrs)


class Log:
    def create_message(self, user='System', action = '', msg = '', host = ''):
        message = ''
        now = time.strftime("%a, %d-%m-%Y %H:%M:%S", time.localtime(time.time()))
        message = 'User %s %s schedule content(%s) in host %s at %s.'%(user, action, msg, host, now)
        return message
    def write():
        pass


#Crontab().append(content='11 11 * * * /bin/sh /home/thomson_crontab/add_aa.sh', override=False)
#Crontab().pop(content='35 15 * * * /bin/sh /home/thomson_crontab/add_aa.sh')
#Crontab().append(Crontab().create(1508144477, '111111', 'start'))
#print Crontab().get_list()
#print CrontabDetail('7 14 18 10 3 sleep 5; /bin/python /script/crontabSMP/job.py -j 13429,13430,13431,13432 -s start').get_pattern()

#print Crontab().get_all()
#print Crontab().create('2017-10-19 11:32:11', '1111', 'start')
#print Crontab().get_cron_by_id(5)

#msg = CrontabDetail('7 14 18 10 3 sleep 5; /bin/python /script/crontabSMP/job.py -j 13429,13430,13431,13432 -s start').human_readable()
#print Log().create_message('system', 'deleted', msg, '172.29.3.189')