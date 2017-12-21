# coding: utf-8
from django.contrib.auth.models import User
from job.models import *
from workflow.models import Workflow as workflow
from setting.MySQL_Database import Database
from setting import DateTime
import json
from setting import settings

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
        sql = "select j.jid, p.name, w.name, j.state, j.status, j.startdate, j.enddate, w.wid from job j \
                INNER JOIN job_param p ON j.jid = p.jid and j.host = '%s'\
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
                INNER JOIN job_param p ON j.jid = p.jid and j.host = '%s'\
                 and j.host = p.host;"%(host)
        return self.db.execute_query(sql)

    # Return Json Job
    def json_job_host(self, thomson_name):
        lstjob = self.get_job_host(thomson_name)
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
        for item in lstjob:
            JId,jobname = item[0], item[1]
            args.append({'jname'    : jobname,
                        'jid'       : JId
                })
        return json.dumps(args)