import json
import time
from xml.dom import minidom
from datetime import datetime
import requests# $ pip install requests
from requests.auth import HTTPDigestAuth
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal

##############################################################################
#                                                                            #
#-----------------------------------LOCAL TIME-------------------------------#
#                                                                            #
##############################################################################

#data input string YYYY-MM-DDTHH:mm:ss.000Z, return a string
def convert_UTC_2_local(utc_time):
    #return UTC fortmat
    ts = time.strptime(utc_time[:19], "%Y-%m-%dT%H:%M:%S")
    dateTime = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    #Convert UTC date to local date
    local_timezone = tzlocal.get_localzone()
    utc_time = datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return str(local_time)[0:len(str(local_time))-6]

##############################################################################
#                                                                            #
#-------------------------------------FILE-----------------------------------#
#                                                                            #
##############################################################################

class File:
    def __init__(self):
        # self.file_path = '/root/thomson_project/setting/responseXml/'
        self.file_path = '/home/huy/django_env/thomson_huynt/setting/responseXml/'

    def read(self, filename):
        print self.file_path + filename
        f = open(self.file_path + filename , 'r')
        lines=f.read()
        f.close()
        #return data
        return lines

    def append(self, filename, text):
        f = open(self.file_path + filename, 'a')
        f.write(text+"\n")
        f.close()

    def get_response(self, filename):
        response = self.read(filename)
        return response

##############################################################################
#                                                                            #
#------------------------------------THOMSON---------------------------------#
#                                                                            #
##############################################################################

class Thomson:
    def __init__(self):
        self.user = 'nguyennt9'
        self.passwd = '123456'
        self.url = 'http://10.0.200.150/services/Maltese'

    def get_response(self, headers, body):
        response = requests.post(self.url, data=body, headers=headers, \
            auth=HTTPDigestAuth(self.user, self.passwd))
        #print response.content
        response_xml = response.content[response.content.find('<soapenv:Envelope') :\
         response.content.find('</soapenv:Envelope>') + len('</soapenv:Envelope>')]
        return response_xml

    def get_datetime(self):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'GetDateAndTime'
        }
        body = """<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:get="GetDateAndTime" xmlns:mal="MalteseGlobal">
                <soapenv:Body>
                    <get:GetDateAndTimeReq Cmd="Start" OpV="01.00.00"/>
                </soapenv:Body>
            </soapenv:Envelope>"""
        reponse_xml = File().get_response('GetDateAndTimeRsp.xml')
        #print reponse_xml
        xmldoc = minidom.parseString(reponse_xml)
        itemlist = xmldoc.getElementsByTagName('GetDateAndTime:RspOkGetDate')
        DateAndTime = itemlist[0].attributes['DateAndTime'].value if \
        'DateAndTime' in str(itemlist[0].attributes.items()) else ""
        OlsonTZ = itemlist[0].attributes['OlsonTZ'].value if \
        'OlsonTZ' in str(itemlist[0].attributes.items()) else ""
        #Convert response data to Json
        args = []
        args.append({'dateAndTime'  : convert_UTC_2_local(DateAndTime) \
            if DateAndTime else "",
                    'timeZone'      : OlsonTZ if OlsonTZ else "Asia/Ho_Chi_Minh"
            })
        return json.dumps(args)

    def get_mountpoint(self):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'GetMountPoints'
        }
        body = """<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:get="GetMountPoints">
              <soapenv:Body>
                <get:GetMountPointsReq Cmd="Start" OpV="01.00.00"/>
              </soapenv:Body>
            </soapenv:Envelope>"""
        #reponse_xml = self.get_response(headers, body)
        reponse_xml = File().get_response('GetMountPointsRsp.xml')
        #print reponse_xml
        xmldoc = minidom.parseString(reponse_xml)
        itemlist = xmldoc.getElementsByTagName('GetMountPoints:MountPoint')
        args = []
        for s in itemlist:
            Name = s.attributes['Name'].value if 'Name' in \
            str(s.attributes.items()) else ""
            args.append({'name'             : Name if Name else ""
                })
        return json.dumps(args)
        
##############################################################################
#                                                                            #
#------------------------------------LOG-------------------------------------#
#                                                                            #
##############################################################################

class Log:
    def __init__(self):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'LogsGet'
        }
        self.headers = headers

    def parse_xml(self, xml):
        xmldoc = minidom.parseString(xml)
        itemlist = xmldoc.getElementsByTagName('lGet:RspAddCl')
        args = []
        for s in itemlist:
            str_tmp = str(s.attributes.items())
            JId = s.attributes['JId'].value if 'JId' in str_tmp else ""
            Cat = s.attributes['Cat'].value if 'Cat' in str_tmp else ""
            LId = s.attributes['LId'].value if 'LId' in str_tmp else ""
            Res = s.attributes['Res'].value if 'Res' in str_tmp else ""
            JName = s.attributes['JName'].value if 'JName' in str_tmp else ""
            NId =  s.attributes['NId'].value if 'NId' in str_tmp else ""
            Sev = s.attributes['Sev'].value if 'Sev' in str_tmp else ""
            Desc = s.attributes['Desc'].value if 'Desc' in str_tmp else ""
            #Convert response data to Json
            args.append({'jid'             : JId,
                        'cat'              : Cat,
                        'lid'              : LId,
                        'res'              : Res,
                        'jname'            : JName,
                        'nid'              : NId,
                        'sev'              : Sev,
                        'desc'             : Desc
                })
        return json.dumps(args)

    #Getting All Logs
    def get_log(self):
        body = """<soapenv:Envelope
xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:log="LogsGet" xmlns:mal="MalteseGlobal"
xmlns:job="JobGlobal">
 <soapenv:Body>
<log:LogsGetReq Cmd="Start" OpV="01.00.00" Open="true"
Close="true" Sys="true" Sev="Info to
critical" Nb="100" PastCloseNb="500"/>
 </soapenv:Body>
</soapenv:Envelope>"""
        #reponse_xml = Thomson().get_response(self.headers, body)
        reponse_xml = File().get_response('LogsAllGetRsp.xml')
        return self.parse_xml(reponse_xml)

    #Getting Open Logs of All Severities
    def get_open(self):
        body = """<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:log="LogsGet" xmlns:mal="MalteseGlobal"
            xmlns:job="JobGlobal">
                <soapenv:Body>
                    <log:LogsGetReq Cmd="Start" OpV="01.00.00" Sev="Info to critical" />
                </soapenv:Body>
            </soapenv:Envelope>"""
        #reponse_xml = Thomson().get_response(self.headers, body)
        reponse_xml = File().get_response('LogsGetRsp.xml')
        print reponse_xml
        return self.parse_xml(reponse_xml)

    #Getting All open log of Specific Jobs
    def get_by_jobID(self, jobID):
        body = """<soapenv:Envelope
xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:log="LogsGet" xmlns:mal="MalteseGlobal"
xmlns:job="JobGlobal">
 <soapenv:Body>
<log:LogsGetReq Cmd="Start" OpV="01.00.00" Open="true"
Close="false" Sys="false" JSelect="Selected jobs" Sev="Info
to critical">
 <job:JId>%d</job:JId>
 </log:LogsGetReq>
</soapenv:Body>
</soapenv:Envelope>"""%(jobID)
        reponse_xml = Thomson().get_response(self.headers, body)
        return self.parse_xml(reponse_xml)

##############################################################################
#                                                                            #
#-----------------------------------WORKFLOW---------------------------------#
#                                                                            #
##############################################################################

class Workflow:
    def __init__(self):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'WorkflowGetList'
        }
        self.headers = headers

    def parse_xml(self, xml):
        xmldoc = minidom.parseString(xml)
        itemlist = xmldoc.getElementsByTagName('wGetList:WItem')
        args=[]
        for s in itemlist:
            str_tmp = str(s.attributes.items())
            Name = s.attributes['Name'].value if 'Name' in str_tmp else ""
            WId = s.attributes['WId'].value if 'WId' in str_tmp else ""
            PubVer = s.attributes['PubVer'].value if 'PubVer' in str_tmp else ""
            PriVer = s.attributes['PriVer'].value if 'PriVer' in str_tmp else ""
            #Convert response data to Json
            args.append({'name'             : Name,
                        'wid'               : WId,
                        'pubver'            : PubVer,
                        'priver'            : PriVer
                })
        return json.dumps(args)   

    def get_workflow(self):
        body = """<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:wor="WorkflowGetList">
                <soapenv:Body>
                    <wor:WorkflowGetListReq Cmd="Start" OpV="01.00.00"/>
                </soapenv:Body>
            </soapenv:Envelope>"""
        #reponse_xml = Thomson().get_response(self.headers, body)
        reponse_xml = File().get_response('WorklowGetListRsp.xml')
        return self.parse_xml(reponse_xml)

class WorkflowDetail:
    def __init__(self, wfid):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'WorkflowGetPublicDesc'
        }
        body = """<soapenv:Envelope
                  xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:wor="WorkflowGetPublicDesc" xmlns:mal="MalteseGlobal">
                    <soapenv:Body>
                      <wor:WorkflowGetPublicDescReq Cmd="Start"
                      OpV="01.00.00">
                        <wor:WInfReq WId="WorkflowUser_DaNang1DuplicatedMyTV"/>
                      </wor:WorkflowGetPublicDescReq>
                    </soapenv:Body>
                  </soapenv:Envelope>"""
        self.headers = headers
        self.body = body
        self.wfid = wfid

    def parse_xml(self, xml):
        xmldoc = minidom.parseString(xml)
        wflist = xmldoc.getElementsByTagName('wd:Workflow')
        wf = wflist[0]
        wfname = wf.attributes['name'].value if 'name' in \
        str(wf.attributes.items()) else ''
        wfid = wf.attributes['id'].value if 'id' in \
        str(wf.attributes.items()) else ''
        wfpriority = wf.attributes['priority'].value if 'priority' in \
        str(wf.attributes.items()) else ''
        wfcategory = wf.attributes['category'].value if 'category' in \
        str(wf.attributes.items()) else ''
        wfcolor = wf.attributes['color'].value if 'color' in \
        str(wf.attributes.items()) else ''
        args_param = []
        paramlist = xmldoc.getElementsByTagName('wd:Param')
        for param in paramlist:
            name = param.attributes['name'].value if 'name' in \
            str(param.attributes.items()) else ''
            value = param.attributes['value'].value if 'value' in \
            str(param.attributes.items()) else ''
            args_param.append({'name'              : name,
                               'value'             : value
                        })
        args = []
        args.append({'id'                      : wfid,
                     'name'                    : wfname,
                     'priority'                : wfpriority,
                     'category'                : wfcategory,
                     'color'                   : wfcolor,
                     'params'                  : args_param
                     })
        return json.dumps(args)

    def get_param(self):
        #reponse_xml = Thomson().get_response(self.headers, self.body)
        reponse_xml = File().get_response('WorkflowGetParamsRsp.xml')
        #print response_xml
        return self.parse_xml(reponse_xml)

##############################################################################
#                                                                            #
#------------------------------------JOB---------------*---------------------#
#                                                                            #
##############################################################################

class Job:
    def __init__(self):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'JobGetList'
        }
        self.headers = headers

    def parse_xml(self, xml):
        xmldoc = minidom.parseString(xml)
        itemlist = xmldoc.getElementsByTagName('jGetList:JItem')
        args=[]
        for s in itemlist:
            str_tmp = str(s.attributes.items())
            State = s.attributes['State'].value if 'State' in str_tmp else ""
            Status = s.attributes['Status'].value if 'Status' in str_tmp else ""
            JId = s.attributes['JId'].value if 'JId' in str_tmp else ""
            Prog = s.attributes['Prog'].value if 'Prog' in str_tmp else ""
            StartDate =  s.attributes['StartDate'].value \
            if 'StartDate' in str_tmp else ""
            Ver = s.attributes['Ver'].value if 'Ver' in str_tmp else ""
            EndDate = s.attributes['EndDate'].value if 'EndDate' in str_tmp else ""
            #Convert response data to Json
            jobname, workflowIdRef = JobDetail(str(JId)).get_job_name() if JId else ''
            args.append({'jname'    : jobname,
                        'wid'       : workflowIdRef,
                        'state'     : State,
                        'status'    : Status,
                        'jid'       : JId,
                        'prog'      : Prog,
                        'startdate' : convert_UTC_2_local(StartDate) \
                        if StartDate else "",
                        'ver'       : Ver,
                        'enddate'   : convert_UTC_2_local(EndDate) \
                        if EndDate else ""
                })
        return json.dumps(args) 

    def get_job(self):
        body = """<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:job="JobGetList" xmlns:job1="JobGlobal">
                <soapenv:Header/>
                <soapenv:Body>
                    <job:JobGetListReq Cmd="Start" OpV="01.00.00" >
                        <job1:JState>Waiting</job1:JState>
                        <job1:JState>Running</job1:JState>
                        <job1:JState>Paused</job1:JState>
                        <job1:JState>Completed</job1:JState>
                        <job1:JState>Aborted</job1:JState>
                    </job:JobGetListReq>
                </soapenv:Body>
            </soapenv:Envelope>"""
        #reponse_xml = Thomson().get_response(self.headers, body)
        reponse_xml = File().get_response('JobGetListRsp.xml')
        return self.parse_xml(reponse_xml)

    def get_Waiting(self):
        body = """<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:job="JobGetList" xmlns:job1="JobGlobal">
                <soapenv:Header/>
                <soapenv:Body>
                    <job:JobGetListReq Cmd="Start" OpV="01.00.00" >
                        <job1:JState>Waiting</job1:JState>
                    </job:JobGetListReq>
                </soapenv:Body>
            </soapenv:Envelope>"""
        reponse_xml = Thomson().get_response(self.headers, body)
        return self.parse_xml(reponse_xml)

    def get_Running(self):
        body = """<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:job="JobGetList" xmlns:job1="JobGlobal">
                <soapenv:Header/>
                <soapenv:Body>
                    <job:JobGetListReq Cmd="Start" OpV="01.00.00" >
                        <job1:JState>Running</job1:JState>
                    </job:JobGetListReq>
                </soapenv:Body>
            </soapenv:Envelope>"""
        #reponse_xml = Thomson().get_response(self.headers, body)
        reponse_xml = File().get_response('JobGetListRsp.xml')
        return self.parse_xml(reponse_xml)

    def get_Paused(self):
        body = """<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:job="JobGetList" xmlns:job1="JobGlobal">
                <soapenv:Header/>
                <soapenv:Body>
                    <job:JobGetListReq Cmd="Start" OpV="01.00.00" >
                        <job1:JState>Paused</job1:JState>
                    </job:JobGetListReq>
                </soapenv:Body>
            </soapenv:Envelope>"""
        #reponse_xml = Thomson().get_response(self.headers, body)
        reponse_xml = File().get_response('JobGetListRsp.xml')
        return self.parse_xml(reponse_xml)

    def get_Completed(self):
        body = """<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:job="JobGetList" xmlns:job1="JobGlobal">
                <soapenv:Header/>
                <soapenv:Body>
                    <job:JobGetListReq Cmd="Start" OpV="01.00.00" >
                        <job1:JState>Completed</job1:JState>
                    </job:JobGetListReq>
                </soapenv:Body>
            </soapenv:Envelope>"""
        #reponse_xml = Thomson().get_response(self.headers, body)
        reponse_xml = File().get_response('JobGetListRsp.xml')
        return self.parse_xml(reponse_xml)

    def get_Aborted(self):
        body = """<soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:job="JobGetList" xmlns:job1="JobGlobal">
                <soapenv:Header/>
                <soapenv:Body>
                    <job:JobGetListReq Cmd="Start" OpV="01.00.00" >
                        <job1:JState>Aborted</job1:JState>
                    </job:JobGetListReq>
                </soapenv:Body>
            </soapenv:Envelope>"""
        #reponse_xml = Thomson().get_response(self.headers, body)
        reponse_xml = File().get_response('JobGetListRsp.xml')
        return self.parse_xml(reponse_xml)

class JobDetail:
    def __init__(self, jid):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'JobGetParams'
        }

        body = """<soapenv:Envelope
                  xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:job="JobGetParams">
                    <soapenv:Body>
                      <job:JobGetParamsReq Cmd="Start" OpV="01.00.00"
                      JId="%s"/>
                    </soapenv:Body>
                  </soapenv:Envelope>"""%(jid)
        self.headers = headers
        self.body = body
        self.jid = jid

    def parse_xml(self, xml):
        xmldoc = minidom.parseString(xml)
        joblist = xmldoc.getElementsByTagName('wd:Job')
        job = joblist[0]
        jobname = job.attributes['name'].value if 'name' in \
        str(job.attributes.items()) else ''
        workflowIdRef = job.attributes['workflowIdRef'].value if \
        'workflowIdRef' in str(job.attributes.items()) else ''
        args_param = []
        paramlist = xmldoc.getElementsByTagName('wd:ParamDesc')
        for param in paramlist:
            name = param.attributes['name'].value if 'name' in \
            str(param.attributes.items()) else ''
            value = param.attributes['value'].value if 'value' in \
            str(param.attributes.items()) else ''
            args_param.append({'name'              : name,
                               'value'             : value
                        })
        args = []
        args.append({'jobname'                      : jobname,
                     'workflowIdRef'                : workflowIdRef,
                     'params'                       : args_param
                     })
        return json.dumps(args)

    def get_param(self):
        #reponse_xml = Thomson().get_response(self.headers, self.body)
        reponse_xml = File().get_response('JobGetParamsRsp.xml')
        #print response_xml
        return self.parse_xml(reponse_xml)


    def get_job_name(self):
        #reponse_xml = Thomson().get_response(self.headers, self.body)
        reponse_xml = File().get_response('JobGetParamsRsp.xml')
        #print response_xml
        xmldoc = minidom.parseString(reponse_xml)
        joblist = xmldoc.getElementsByTagName('wd:Job')
        job = joblist[0]
        jobname = job.attributes['name'].value if 'name' in \
        str(job.attributes.items()) else ''
        workflowIdRef = job.attributes['workflowIdRef'].value if \
        'workflowIdRef' in str(job.attributes.items()) else ''
        return jobname, workflowIdRef


##############################################################################
#                                                                            #
#------------------------------------MAIN------------------------------------#
#                                                                            #
##############################################################################

#if __name__ == "__main__":
    #print Thomson().get_datetime()
    #print Thomson().get_mountpoint()
    #print Log().get_log()
    #print Log().get_open()
    #print Job().get_Running()
    #Log().get_log()
    #Log().get_by_jobID(12810)
    #print Workflow().get_workflow()
    #Job().get_Running()
    #print WorkflowDetail('dsg').get_param()
