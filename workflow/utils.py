from django.contrib.auth.models import User
from job.models import *
from setting.MySQL_Database import Database
import json
from setting import settings
class DatabaseWorkflow():
    """docstring for DataBaseWorkflow"""
    def __init__(self):
        # super (DataBaseWorkflow, self).__init__()
        self.db = Database()

    def get_all_workflow(self, thomson_name):
        host = settings.THOMSON_HOST[thomson_name]['host']
        sql = "select name, wid from workflow where host = '%s';"%(host)
        # print self.db.execute_query(sql)
        return self.db.execute_query(sql)

    def  json_all_workflow(self, thomson_name):
        lstworkflow = self.get_all_workflow(thomson_name)
        args=[]
        for item in lstworkflow:
            Name = item[0]
            WId = item[1]
            # PubVer = s.attributes['PubVer'].value if "'PubVer'" in str_tmp else ''
            # PriVer = s.attributes['PriVer'].value if "'PriVer'" in str_tmp else ''
            #Convert response data to Json
            args.append({'name'             : Name if Name else '',
                        'wid'               : WId if WId  else ''
                        # 'pubver'            : int(PubVer),
                        # 'priver'            : int(PriVer)
                })
        # print args
        return json.dumps(args)   