# coding: utf-8
import subprocess
import os
import time
from datetime import datetime
import re
import json
from setting.get_thomson_api import *

class Crontab:

    def create(self, date_time, jobid, action):
        if not date_time.isdigit():
            try:
                date_time = int(time.mktime(time.strptime(date_time, '%Y-%m-%d %H:%M:%S')))
            except Exception as e:
                return None
        dt=datetime.fromtimestamp(date_time)
        #print dt
        DD = dt.day
        MM = dt.month
        hh = dt.hour
        print hh
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

    def pop(self, content=''):
        if not content:
            raise ValueError('neither filename or crontab must be specified')
        else:
            content = content.strip()
        installed_content =  self.get_list()
        if not installed_content:
            return 'Crontab is not available'
        new_crontab = ''
        for old_crontab in installed_content.split('\n'):
            if old_crontab != content:
                new_crontab += '\n%s' % old_crontab
        if new_crontab:
            new_crontab += '\n'
        # install back
        retcode, err, out = self._runcmd('crontab', new_crontab)
        if retcode != 0: 
            raise ValueError('failed to install crontab, check if crontab is valid')

    def get_all(self):
        list_task = self.get_list()
        id = 0
        agrs = []
        for task in list_task.split('\n'):
            id+=1
            schedule = ReadCrontab(task).serialization()
            if schedule:
                ss,mm,hh,DD,MM,YYYY,dayofweek,list_jid,action,full_date,state,alarm = ReadCrontab(schedule).get_pattern()
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

    
class ReadCrontab:
    def __init__(self, task):
        self.task = task
    def serialization(self):
        cron_pattern=re.compile("[ ?\d{1,2}]*\ sleep \d{1,2}; /bin/python /script/crontabSMP/job.py -[Jj] [,?\d{3,10}]*\ -[Ss] (?:[Ss]tart|[Ss]top)")
        #cron_pattern=re.compile("\d{1,2}\ \d{1,2}\ \d{1,2}\ \d{1,2}\ \d{1,2}\ sleep \d{1,2}; /bin/python /script/crontabSMP/job.py -[Jj] \d{3,10}\ -[Ss] (?:[Ss]tart|[Ss]top)")
        cron = re.findall(cron_pattern, self.task)
        if cron:
            return cron[0]
        else:
            return None
    def get_unix_timestamp(self, ss, mm, hh, DD, MM, YYYY):
        human_date = "%s-%s-%s %s:%s:%s"%(YYYY,MM,DD,hh,mm,ss)
        return (int(time.mktime(time.strptime(human_date, '%Y-%m-%d %H:%M:%S'))) - time.timezone)

#state = 0: schedule complete
#state = 1: schedule waiting

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
        state = 0
        jid_pattern = re.compile("\d{3,10}")    
        list_jid = re.findall(jid_pattern, cron)
        reaction_pattern = re.compile("(?:-[Ss] [Ss]tart|-[Ss] [Ss]top)")
        action_pattern = re.compile("([Ss]tart|[Ss]top)")
        reaction = re.findall(reaction_pattern, cron)
        if reaction:
            action = re.findall(action_pattern, reaction[0])
            action = action[0]
        full_date = self.get_unix_timestamp(ss,mm,hh,DD,MM,YYYY)
        now = time.time() - time.timezone
        minus_dt = full_date - now
        if minus_dt > 0:
            mm, ss = divmod(minus_dt, 60)
            hh, mm = divmod(mm, 60)
            alarm = "%d:%02d:%02d" % (hh, mm, ss)
            state = 1
        return ss,mm,hh,DD,MM,YYYY,dayofweek,list_jid,action,full_date,state,alarm
#Crontab().append(content='11 11 * * * /bin/sh /home/thomson_crontab/add_aa.sh', override=False)
#Crontab().pop(content='35 15 * * * /bin/sh /home/thomson_crontab/add_aa.sh')
#Crontab().append(Crontab().create(1508144477, '111111', 'start'))
#print Crontab().get_list()
#print ReadCrontab('7 14 18 10 3 sleep 5; /bin/python /script/crontabSMP/job.py -j 13429,13430,13431,13432 -s start').get_pattern()

#print Crontab().get_all()
#print Crontab().create('2017-10-19 11:32:11', '1111', 'start')