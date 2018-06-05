# coding: utf-8
from django.contrib.auth.models import User
from job.models import *
from workflow.models import Workflow as workflow
from setting.MySQL_Database import Database
from setting import DateTime
import json
from setting import settings
from setting import logger
import logging, logging.config

import time

class DatabaseJob():
    """docstring for RequsetGetJob"""
    def __init__(self):
        self.db = Database()
        # super(RequsetGetJob, self).__init__()

    #Query Job
    def get_all_job(self):
        sql = "select j.jid, p.name, w.name, j.state, j.status, j.startdate, j.enddate, w.wid from job j \
                INNER JOIN job_param p ON j.jid = p.jid and j.host = p.host\
                INNER JOIN workflow w ON w.wid = p.wid and w.host = p.host;"
        return self.db.execute_query(sql)

    def get_job_host(self, thomson_name):
        host = settings.THOMSON_HOST[thomson_name]['host']
        sql = "select j.jid, p.name, w.name, j.state, j.status, j.startdate, j.enddate, w.wid, j_a.auto from job j \
                LEFT JOIN job_auto j_a ON j.jid = j_a.jid and j.host = j_a.host\
                INNER JOIN job_param p ON j.jid = p.jid and p.host = j.host and p.host = '%s'\
                INNER JOIN workflow w ON w.wid = p.wid and w.host = p.host;"%(host)
        # result = {}
        # lst = self.db.execute_query(sql)
        # for item in lst:
        #     args = []
        #     args.append(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])
        #     result
        return self.db.execute_query(sql)

    def get_job_name(self, thomson_name):
        host = settings.THOMSON_HOST[thomson_name]['host']
        sql = "select j.jid, p.name from job j \
                INNER JOIN job_param p ON j.jid = p.jid and p.host = '%s'\
                 and j.host = p.host;"%(host)
        return self.db.execute_query(sql)

    def update_job_auto(self, thomson_name, data):
        """"
        update status auto return main job
        data: json {'jticket':,'jid':}
        """
        host = settings.THOMSON_HOST[thomson_name]['host']
        sql_update = "update job_auto set auto = %s where jid = %d and host = '%s';"%(data['jticked'], data['jid'], host)
        sql_insert = "insert into job_auto (jid, host, auto) values(%d, %s,%s);"%(data['jid'], host, data['jticked'])
        if self.check_job_auto(host, data['jid']):
            sql = sql_update
        else:
            sql = sql_insert
        # print sql
        return self.db.execute_non_query(sql)
    
    def check_job_auto(self, host, jid):
        """
        kiem tra jid da co ton tai trong database
        return true/false
        """
        sql = "select jid from job_auto where jid= %d and host = '%s';"%(jid, host)
        if len(self.db.execute_query(sql)):
            return 1
        else: return 0

    # Return Json Job
    def json_job_host(self, thomson_name):
        lstjob = self.get_job_host(thomson_name)
        args=[]
        # print len(lstjob)
        if not lstjob:
            time.sleep(1)
            lstjob = self.get_job_host(thomson_name)
            print "no data list job by host"
        for item in lstjob:
            JId,jobname,workflow_name,State,Status,StartDate,EndDate,workflowIdRef,backMain = item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]
            args.append({'jname'    : jobname,
                        'wid'       : workflowIdRef,
                        'wname'     : workflow_name,
                        'state'     : State,
                        'status'    : Status,
                        'jid'       : JId,
                        # 'prog'      : int(Prog),
                        'startdate' : StartDate \
                        if StartDate else None,
                        # 'ver'       : int(Ver),
                        'enddate'   : EndDate \
                        if EndDate else None,
                        'iauto'     : backMain
                })
        return json.dumps(args)

    def json_all_job(self):
        lstjob = self.get_all_job()
        args=[]
        for item in lstjob:
            JId,jobname,workflow_name,State,Status,StartDate,EndDate,workflowIdRef = item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]
            args.append({'jname'    : jobname,
                        'wid'       : workflowIdRef,
                        'wname'     : workflow_name,
                        'state'     : State,
                        'status'    : Status,
                        'jid'       : JId,
                        # 'prog'      : int(Prog),
                        'startdate' : StartDate \
                        if StartDate else None,
                        # 'ver'       : int(Ver),
                        'enddate'   : EndDate \
                        if EndDate else None
                })
        return json.dumps(args)

    def json_job_name(self, thomson_name):
        lstjob = self.get_job_name(thomson_name)
        args=[]
        if not lstjob:
            time.sleep(1)
            lstjob = self.get_job_name(thomson_name)
            print "no data list job by name"
        for item in lstjob:
            JId,jobname = item[0], item[1]
            args.append({'jname'    : jobname,
                        'jid'       : JId
                })
        return json.dumps(args)

    def count_job_host(self, thomson_name):
        args=[]
        host = settings.THOMSON_HOST[thomson_name]['host']
        total = Job.objects.filter(host = host).count()
        running = Job.objects.filter(host = host, state='running').count()
        args.append({'total':   total,'running':   running})
        return json.dumps(args)

    # check job backup True/False
    def check_backup_job(self, thomson_name, jid):
        host = settings.THOMSON_HOST[thomson_name]['host']
        return JobParam.objects.filter(host = host, jid = jid)[0].backup

class History:
    """docstring for JobHistory"""
    def create_log(self, thomson_name, user, action, jid, datetime, des=None):
        log = logging.getLogger("thomson-tool")
        host = settings.THOMSON_HOST[thomson_name]['host']
        jname = JobParam.objects.all().filter(host = host, jid = jid)[0].name
        desc = "Job operation: %s by \"%s\" from Thomson-Tool"%(action, user)
        args = {"sev": "Info", "host": host, "opdate": datetime, "jid": jid, "jname": jname, "desc": desc}
        log.critical(json.dumps(args))
        history = JobHistory(user=user, host=host, action=action, jid=jid, datetime=datetime)
        history.save()
        print "log start/stop job"
