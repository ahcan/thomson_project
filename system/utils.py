from django.contrib.auth.models import User
from system.models import Node
from job.models import Job
from setting.MySQL_Database import Database
import json
from setting import settings
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
        for node in lstnodes:
            jerror, jcounter = self.count_job_error(node.host)
            args.append({'status'        :node.status,
                        'cpu'           :node.cpu,
                        'alloccpu'      :node.alloccpu,
                        'mem'           :node.mem,
                        'allocmem'      :node.allocmem,
                        'nid'           :node.nid,
                        'uncreahable'   :node.uncreachable,
                        'state'         :node.state,
                        'jerror'        :jerror,
                        'jcounter'      :jcounter})
        return json.dumps(args)

    def count_job_error(self, host):
        # print self.host
        job_list = Job.objects.all().filter(host=host)
        error=0
        for job in job_list:
            if job.status != 'Ok':
                error += 1
        return error, len(job_list)