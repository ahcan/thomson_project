from django.contrib.auth.models import User
from system.models import Node, NodeDetail
from job.models import Job
from setting.MySQL_Database import Database
import json
from setting import settings
import time
class DatabaseNode():
    """docstring for DataBaseWorkflow"""
    def __init__(self, thomson_name):
        # super (DataBaseWorkflow, self).__init__()
        # self.db = Database()
        self.host = settings.THOMSON_HOST[thomson_name]['host']

    def get_all_node(self):
        return Node.objects.all().filter(host=self.host)

    def get_all_node_json(self):
        lstnodes = self.get_all_node()
        args=[]
        job_list = Job.objects.all().filter(host=self.host).exclude(status='Ok')
        # print self.host
        if not lstnodes:
            time.sleep(1)
            lstnodes = self.get_all_node()
        for node in lstnodes:
            jerror, jcounter, jobs_error= self.count_job_error(node.host, node.nid)
            args.append({'status'        :node.status,
                        'cpu'           :node.cpu,
                        'alloccpu'      :node.alloccpu,
                        'mem'           :node.mem,
                        'allocmem'      :node.allocmem,
                        'nid'           :node.nid,
                        'uncreahable'   :node.uncreachable,
                        'state'         :node.state,
                        'jerror'        :jerror,
                        'jcounter'      :jcounter,
                        'jobs'          :jobs_error})
        return json.dumps(args)

    # count job error
    def count_job_error(self, host, nid):
        # print self.host
        # get all job error
        job_list = Job.objects.all().filter(host=host).exclude(status='Ok')
        jobs_error = []
        # print job_list[0].status
        # print len(job_list)
        job_node = NodeDetail.objects.all().filter(host=host, nid=nid)
        error=0
        for item in job_node:
            for job in job_list:
                if item.jid == job.jid:
                    error += 1
                    jobs_error.append(job.jid)
                    break
        return error, len(job_node), jobs_error

    def get_node_by_job(self, jid):
        tmp = NodeDetail.objects.filter(host= self.host, jid=jid)
        if not tmp:
            time.sleep(1)
            tmp = NodeDetail.objects.filter(host= self.host, jid=jid)
        try:
            result = tmp[0].nid
        except Exception as e:
            result = e
        return result