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
    print utc_time
    #return UTC fortmat
    ts = time.strptime(utc_time[:19], "%Y-%m-%dT%H:%M:%S")
    human_date = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    return (int(time.mktime(time.strptime(human_date, '%Y-%m-%d %H:%M:%S'))) - time.timezone)
    #Convert UTC date to local date
    #local_timezone = tzlocal.get_localzone()
    #utc_time = datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
    #local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    #return str(local_time)[0:len(str(local_time))-6]

##############################################################################
#                                                                            #
#-------------------------------------FILE-----------------------------------#
#                                                                            #
##############################################################################

class File:
    def __init__(self):
        #self.file_path = '/root/thomson_project/setting/responseXml/'
        self.file_path = 'setting/responseXml/'
        #self.file_path = '/home/huy/django_env/thomson_huynt/setting/responseXml/'

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
        self.url = 'http://172.29.3.189/services/Maltese'

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
        #response_xml = self.get_response(headers, body)
        response_xml = File().get_response('GetDateAndTimeRsp.xml')
        #print response_xml
        xmldoc = minidom.parseString(response_xml)
        itemlist = xmldoc.getElementsByTagName('GetDateAndTime:RspOkGetDate')
        DateAndTime = itemlist[0].attributes['DateAndTime'].value if \
        "'DateAndTime'" in str(itemlist[0].attributes.items()) else ""
        OlsonTZ = itemlist[0].attributes['OlsonTZ'].value if \
        "'OlsonTZ'" in str(itemlist[0].attributes.items()) else ""
        #Convert response data to Json
        args = []
        args.append({'dateAndTime'  : convert_UTC_2_local(DateAndTime) \
            if DateAndTime else 1,
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
        #response_xml = self.get_response(headers, body)
        response_xml = File().get_response('GetMountPointsRsp.xml')
        #print response_xml
        xmldoc = minidom.parseString(response_xml)
        itemlist = xmldoc.getElementsByTagName('GetMountPoints:MountPoint')
        args = []
        for s in itemlist:
            Name = s.attributes['Name'].value if "'Name'" in \
            str(s.attributes.items()) else ""
            args.append({'name'             : Name if Name else ""
                })
        return json.dumps(args)

    def get_system_status(self):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'SystemGetStatus'
        }

        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
          <s:Body>
            <ns67:SystemGetStatusReq xmlns:ns67="SystemGetStatus" Cmd="Start" OpV="01.00.00">
            </ns67:SystemGetStatusReq>
           </s:Body>
        </s:Envelope>"""
        #response_xml = self.get_response(headers, body)
        response_xml = File().get_response('SystemGetStatusRsp.xml')
        xmldoc = minidom.parseString(response_xml)
        itemlist = xmldoc.getElementsByTagName('sGetStatus:RspOkSGS')
        Status = itemlist[0].attributes['Status'].value if 'Status' in\
         str(itemlist[0].attributes.items()) else ""
        CPU = itemlist[0].attributes['CPU'].value if "'CPU'" in\
         str(itemlist[0].attributes.items()) else '-1'
        Mem = itemlist[0].attributes['Mem'].value if "'Mem'" in\
         str(itemlist[0].attributes.items()) else '-1'
        agrs = []
        agrs.append({'status': Status,
                     'cpu'   : int(CPU),
                     'mem'   : int(Mem)
                    })
        return json.dumps(agrs)

    def get_job_status(self):
        agrs = []
        agrs.append({
            'total'     :Job().count_job(),
            'running'   :Job().count_Running(),
            'completed' :Job().count_Completed(),
            'waiting'   :Job().count_Waiting(),
            'paused'    :Job().count_Paused(),
            'aborted'   :Job().count_Aborted()
            })
        return json.dumps(agrs)


##############################################################################
#                                                                            #
#------------------------------------NODES-----------------------------------#
#                                                                            #
##############################################################################

class Node:
    def __init__(self):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'SystemGetNodesStats'
        }

        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
          <s:Body>
            <ns67:SystemGetNodesStatsReq xmlns:ns67="SystemGetNodesStats" Cmd="Start" OpV="01.00.00">
            </ns67:SystemGetNodesStatsReq>
           </s:Body>
        </s:Envelope>"""

        self.headers = headers
        self.body = body

    def get_nodes_xml(self):
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'SOAPAction': 'SystemGetNodesStats'
        }

        body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
          <s:Body>
            <ns67:SystemGetNodesStatsReq xmlns:ns67="SystemGetNodesStats" Cmd="Start" OpV="01.00.00">
            </ns67:SystemGetNodesStatsReq>
           </s:Body>
        </s:Envelope>"""
        #response_xml = Thomson().get_response(headers, body)
        response_xml = File().get_response('SystemGetNodesStatsRsp.xml')
        return response_xml

    def parse_dom_object(self, dom_object):
        text = str(dom_object.attributes.items())
        NStatus = dom_object.attributes['NStatus'].value if "'NStatus'" in text else ''
        Cpu = dom_object.attributes['Cpu'].value if "'Cpu'" in text else '-1'
        Unreachable = dom_object.attributes['Unreachable'].value if "'Unreachable'" in text else ''
        NId = dom_object.attributes['NId'].value if "'NId'" in text else '-1'
        NState = dom_object.attributes['NState'].value if "'NState'" in text else ''
        Mem =  dom_object.attributes['Mem'].value if "'Mem'" in text else '-1'
        return NStatus,Cpu,Unreachable,NId,NState,Mem

    def parse_xml(self, xml):
        args = []
        xmldoc = minidom.parseString(xml)
        itemlist = xmldoc.getElementsByTagName('sGetNodesStats:RspSGNSOk')
        for node in itemlist.item(0).childNodes:
            NStatus,Cpu,Unreachable,NId,NState,Mem = self.parse_dom_object(node)
            JError, JCounter = NodeDetail(NId).count_job_error()
            args.append({'status'             : NStatus,
                        'cpu'                 : int(Cpu),
                        'uncreahable'         : Unreachable,
                        'nid'                 : int(NId),
                        'state'               : NState,
                        'mem'                 : int(Mem),
                        'jerror'              : JError,
                        'jcounter'            : JCounter
                })
        return json.dumps(args)

    def get_info(self):
        xml = self.get_nodes_xml()
        return self.parse_xml(xml)

class NodeDetail:

    def __init__(self, node_id):
        self.nid = int(node_id)

    def get_dom_node(self):
        dom_node = None
        nodes_xml = Node().get_nodes_xml()
        xmldoc = minidom.parseString(nodes_xml)
        itemlist = xmldoc.getElementsByTagName('sGetNodesStats:RspSGNSOk')
        for node in itemlist.item(0).childNodes:
            text = str(node.attributes.items())
            NId = node.attributes['NId'].value if "'NId'" in text else -1
            if int(NId) == self.nid:
                dom_node = node
        return dom_node

    def get_array_job_id(self):
        array_jid = []
        dom_node = self.get_dom_node()
        for node_status_detail in dom_node.childNodes:
            text = str(node_status_detail.attributes.items())
            jid = node_status_detail.attributes['JId'].value if "'JId'" in text else ''
            if jid:
                array_jid.append(int(jid))
        return array_jid

    def get_list_job(self):
        args = []
        array_jid = self.get_array_job_id()
        dom_node = self.get_dom_node()
        NStatus,Cpu,Unreachable,NId,NState,Mem = Node().parse_dom_object(dom_node)
        JError, JCounter = self.count_job_error()
        job_list = Job().get_job_detail_by_job_id(array_jid)
        args.append({'status'             : NStatus,
                    'cpu'                 : int(Cpu),
                    'uncreahable'         : Unreachable,
                    'nid'                 : int(NId),
                    'state'               : NState,
                    'mem'                 : int(Mem),
                    'jerror'              : JError,
                    'jcounter'            : JCounter,
                    'job_list'            : job_list
            })
        return json.dumps(args)

    def count_job_error(self):
        array_jid = self.get_array_job_id()
        job_list = Job().get_job_detail_by_job_id(array_jid)
        error=0
        for job in job_list:
            if job['status'] != 'Ok':
                error += 1
        return error, len(array_jid)
        
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
        args = []
        xmldoc = minidom.parseString(xml)
        itemlist = xmldoc.getElementsByTagName('lGet:RspOkLog')
        for log in itemlist.item(0).childNodes:
            text = str(log.attributes.items())
            JId = log.attributes['JId'].value if "'JId'" in text else '-1'
            Cat = log.attributes['Cat'].value if "'Cat'" in text else ''
            LId = log.attributes['LId'].value if "'LId'" in text else ''
            try:
                Res = log.attributes['Res'].value if "'Res'" in text else ''
            except Exception as e:
                Res = ''
                print text
            #Res = log.attributes['Res'].value if 'Res' in text else ''
            JName = log.attributes['JName'].value if "'JName'" in text else ''
            NId =  log.attributes['NId'].value if "'NId'" in text else ''
            Sev = log.attributes['Sev'].value if "'Sev'" in text else ''
            Desc = log.attributes['Desc'].value if "'Desc'" in text else ''
            OpDate = log.attributes['OpDate'].value if "'OpDate'" in text else ''
            ClDate = log.attributes['ClDate'].value if "'ClDate'" in text else ''
            text = ''
            #Convert response data to Json
            args.append({'jid'             : int(JId),
                        'cat'              : Cat,
                        'lid'              : int(LId),
                        'res'              : Res,
                        'jname'            : JName,
                        'nid'              : int(NId),
                        'sev'              : Sev,
                        'desc'             : Desc,
                        'opdate'           : OpDate,
                        'cldate'           : ClDate
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
                      Close="true" Sys="true" Sev="Info to critical" Nb="500"
                      PastCloseNb="500"/>
                    </soapenv:Body>
                  </soapenv:Envelope>"""
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('LogsAllGetRsp.xml')
        return self.parse_xml(response_xml)

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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('LogsOpenGetRsp.xml')
        print response_xml
        return self.parse_xml(response_xml)

    #Getting All open log of Specific Jobs
    def get_by_jobID(self, jobID):
        body="""<soapenv:Envelope
         xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
         xmlns:log="LogsGet" xmlns:mal="MalteseGlobal" xmlns:job="JobGlobal">
          <soapenv:Body>
            <log:LogsGetReq Cmd="Start" OpV="01.00.00" Open="true"
             Close="true" Sys="true" JSelect="Selected jobs"
             Sev="Info to critical" Nb="30" PastCloseNb="500">
              <job:JId>%d</job:JId>
            </log:LogsGetReq>
          </soapenv:Body>
        </soapenv:Envelope>"""%(jobID)
        response_xml = File().get_response('LogsGetByJobIDRsp.xml')
        #response_xml = Thomson().get_response(self.headers, body)
        return self.parse_xml(response_xml)

    def get_sys_log(self):
        body="""<soapenv:Envelope
         xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
         xmlns:log="LogsGet" xmlns:mal="MalteseGlobal" xmlns:job="JobGlobal">
          <soapenv:Body>
            <log:LogsGetReq Cmd="Start" OpV="01.00.00" Sys="true" Nb="30" PastCloseNb="500"/>
          </soapenv:Body>
        </soapenv:Envelope>"""
        response_xml = File().get_response('LogsGetSysRsp.xml')
        #response_xml = Thomson().get_response(self.headers, body)
        return self.parse_xml(response_xml)


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
            Name = s.attributes['Name'].value if "'Name'" in str_tmp else ''
            WId = s.attributes['WId'].value if "'WId'" in str_tmp else ''
            PubVer = s.attributes['PubVer'].value if "'PubVer'" in str_tmp else ''
            PriVer = s.attributes['PriVer'].value if "'PriVer'" in str_tmp else ''
            #Convert response data to Json
            args.append({'name'             : Name,
                        'wid'               : WId,
                        'pubver'            : int(PubVer),
                        'priver'            : int(PriVer)
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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('WorklowGetListRsp.xml')
        return self.parse_xml(response_xml)

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
                        <wor:WInfReq WId="%s"/>
                      </wor:WorkflowGetPublicDescReq>
                    </soapenv:Body>
                  </soapenv:Envelope>"""%(wfid)
        self.headers = headers
        self.body = body
        self.wfid = wfid

    def parse_xml(self, xml):
        xmldoc = minidom.parseString(xml)
        wflist = xmldoc.getElementsByTagName('wd:Workflow')
        wf = wflist[0]
        wfname = wf.attributes['name'].value if "'name'" in \
        str(wf.attributes.items()) else ''
        wfid = wf.attributes['id'].value if "'id'" in \
        str(wf.attributes.items()) else ''
        wfpriority = wf.attributes['priority'].value if "'priority'" in \
        str(wf.attributes.items()) else ''
        wfcategory = wf.attributes['category'].value if "'category'" in \
        str(wf.attributes.items()) else ''
        wfcolor = wf.attributes['color'].value if "'color'" in \
        str(wf.attributes.items()) else ''
        args_param = []
        paramlist = xmldoc.getElementsByTagName('wd:Param')
        for param in paramlist:
            name = param.attributes['name'].value if "'name'" in \
            str(param.attributes.items()) else ''
            value = param.attributes['value'].value if "'value'" in \
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
        #response_xml = Thomson().get_response(self.headers, self.body)
        response_xml = File().get_response('WorkflowGetParamsRsp.xml')
        #print response_xml
        return self.parse_xml(response_xml)

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

    def parse_dom_object(self, dom_object):
        str_tmp = str(dom_object.attributes.items())
        State = dom_object.attributes['State'].value if "'State'" in str_tmp else ''
        Status = dom_object.attributes['Status'].value if "'Status'" in str_tmp else ''
        JId = dom_object.attributes['JId'].value if "'JId'" in str_tmp else ''
        Prog = dom_object.attributes['Prog'].value if "'Prog'" in str_tmp else ''
        StartDate =  dom_object.attributes['StartDate'].value \
        if "'StartDate'" in str_tmp else ''
        Ver = dom_object.attributes['Ver'].value if "'Ver'" in str_tmp else ''
        EndDate = dom_object.attributes['EndDate'].value if "'EndDate'" in str_tmp else ''
        jobname, workflowIdRef = JobDetail(str(JId)).get_job_name() if JId else ''
        return State,Status,JId,Prog,StartDate,EndDate,Ver,jobname,workflowIdRef

    def parse_xml(self, xml):
        xmldoc = minidom.parseString(xml)
        itemlist = xmldoc.getElementsByTagName('jGetList:JItem')
        args=[]
        for s in itemlist:
            State,Status,JId,Prog,StartDate,EndDate,Ver,jobname,workflowIdRef = self.parse_dom_object(s)
            args.append({'jname'    : jobname,
                        'wid'       : workflowIdRef,
                        'state'     : State,
                        'status'    : Status,
                        'jid'       : int(JId),
                        'prog'      : int(Prog),
                        'startdate' : convert_UTC_2_local(StartDate) \
                        if StartDate else '',
                        'ver'       : int(Ver),
                        'enddate'   : convert_UTC_2_local(EndDate) \
                        if EndDate else ''
                })
        return json.dumps(args)

    def count_object(self, xml):
        xmldoc = minidom.parseString(xml)
        itemlist = xmldoc.getElementsByTagName('jGetList:JItem')
        return len(itemlist)


    def get_job_xml(self):
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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return response_xml

    def get_job(self):
        response_xml = self.get_job_xml()
        return self.parse_xml(response_xml)

    def count_job(self):
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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return self.count_object(response_xml)

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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return self.parse_xml(response_xml)

    def count_Waiting(self):
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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return self.count_object(response_xml)

    def get_Running_xml(self):
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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return response_xml

    def get_Running(self):
        xml = self.get_Running_xml()
        return self.parse_xml(xml)

    def count_Running(self):
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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return self.count_object(response_xml)

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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return self.parse_xml(response_xml)

    def count_Paused(self):
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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return self.count_object(response_xml)

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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return self.parse_xml(response_xml)

    def count_Completed(self):
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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return self.count_object(response_xml)

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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return self.parse_xml(response_xml)

    def count_Aborted(self):
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
        #response_xml = Thomson().get_response(self.headers, body)
        response_xml = File().get_response('JobGetListRsp.xml')
        return self.count_object(response_xml)

    def get_job_detail_by_job_id(self, arr_job_id):
        print arr_job_id
        job_xml = self.get_job_xml()
        xmldoc = minidom.parseString(job_xml)
        itemlist = xmldoc.getElementsByTagName('jGetList:JItem')
        args=[]
        for job in itemlist:
            str_tmp = str(job.attributes.items())
            JId = job.attributes['JId'].value if "'JId'" in str_tmp else '-1'
            if int(JId) in arr_job_id:
                State,Status,JId,Prog,StartDate,EndDate,Ver,jobname,workflowIdRef = self.parse_dom_object(job)
                args.append({'jname'    : jobname,
                            'wid'       : workflowIdRef,
                            'state'     : State,
                            'status'    : Status,
                            'jid'       : JId,
                            'prog'      : Prog,
                            'startdate' : convert_UTC_2_local(StartDate) \
                            if StartDate else '',
                            'ver'       : Ver,
                            'enddate'   : convert_UTC_2_local(EndDate) \
                            if EndDate else ''
                    })
        return args

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
        jobname = job.attributes['name'].value if "'name'" in \
        str(job.attributes.items()) else ''
        workflowIdRef = job.attributes['workflowIdRef'].value if \
        "'workflowIdRef'" in str(job.attributes.items()) else ''
        args_param = []
        paramlist = xmldoc.getElementsByTagName('wd:ParamDesc')
        for param in paramlist:
            name = param.attributes['name'].value if "'name'" in \
            str(param.attributes.items()) else ''
            value = param.attributes['value'].value if "'value'" in \
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
        #response_xml = Thomson().get_response(self.headers, self.body)
        response_xml = File().get_response('JobGetParamsRsp.xml')
        #print response_xml
        return self.parse_xml(response_xml)


    def get_job_name(self):
        #response_xml = Thomson().get_response(self.headers, self.body)
        response_xml = File().get_response('JobGetParamsRsp.xml')
        #print response_xml
        xmldoc = minidom.parseString(response_xml)
        joblist = xmldoc.getElementsByTagName('wd:Job')
        job = joblist[0]
        jobname = job.attributes['name'].value if "'name'" in \
        str(job.attributes.items()) else ''
        workflowIdRef = job.attributes['workflowIdRef'].value if \
        "'workflowIdRef'" in str(job.attributes.items()) else ''
        return jobname, workflowIdRef


##############################################################################
#                                                                            #
#------------------------------------MAIN------------------------------------#
#                                                                            #
##############################################################################

#if __name__ == "__main__":
    #print Thomson().get_nodes_status()
    #print Thomson().get_datetime()
    #print Thomson().get_mountpoint()
    #print Log().get_log()
    #print Log().get_open()
    #print Job().get_Running()
    #Log().get_log()
    #print Log().get_by_jobID(530)
    #print Workflow().get_workflow()
    #Job().get_Running()
    #print WorkflowDetail('dsg').get_param()
    #print Thomson().get_system_status()
    #print Thomson().get_job_status()

