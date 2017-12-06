
from django.contrib.auth.models import User
from job.models import *
from setting.MySQL_Database import Database
import json

class DatabaseWorkflow():
    """docstring for DataBaseWorkflow"""
    def __init__(self):
        # super (DataBaseWorkflow, self).__init__()
        self.db = Database()

    def get_all_workflow(self):
        sql = "select name, wid from workflow;"
        # print self.db.execute_query(sql)
        return self.db.execute_query(sql)

    def  json_all_workflow(self):
        lstworkflow = self.get_all_workflow()
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
        print args
        return json.dumps(args)   