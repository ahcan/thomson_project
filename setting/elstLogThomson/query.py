from elasticsearch import Elasticsearch
import json
import re
from setting import DateTime

class Elastic:

    def __init__(self, host=None, port = 9200, size = 1000, index='_all', *args, **kwargs):
        """
        :host: ip elasticsearch
        :port: port of elasticsearch server (default 9200)
        :ident: tu khoa dung de match du lieu
        :size: so luong data lay ra (default 500)
        :index: index of elasticsearch
        :ip: ip address thomson
        """
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                self.key = value
        self.host = host
        self.port = port
        self.size = size
        self.index = index
        return

    def query_by_ident(self, ident=None, time = "66m", size = 0, ip = 0):
        """
        time: thoi gian loc log tu hien tai minute(m),hour(h), day(d)...
        ip: ip address for match
        Return array full log by ident
        """
        self.size = size if size else self.size
        self.ip = ip if ip else self.ip
        now = DateTime.DateTime()
        timesindex = now.get_date_as_human_creadeble()
        # timestamp = now.get_now_as_isofortmat()
        # print timestamp
        query = {
            "sort": [{"@timestamp": "desc"}],
            "from": 0,
            "size": self.size,
            "_source": ["message"],
            "query": {
                "bool": {
                "must": [
                    {
                    "bool": {
                        "should": [
                        {
                            "bool": {
                            "should": [
                                {
                                "bool": {
                                    "must": [
                                    {
                                        "match": {
                                        "ident.keyword": "Monitor"
                                        }
                                    },
                                    {
                                        "match": {
                                        "message": "origin"
                                        }
                                    },
                                    {
                                        "match": {
                                        "message": "%s"%(ident)
                                        }
                                    }
                                    ]
                                }
                                },
                                {
                                "bool": {
                                    "must": [
                                    {
                                        "match": {
                                        "ident.keyword": "Monitor"
                                        }
                                    },
                                    {
                                        "match": {
                                        "message": "4500"
                                        }
                                    }
                                    ]
                                }
                                }
                            ]
                            }
                        },
                        {
                            "bool": {
                            "should": [
                                {
                                "bool": {
                                    "must": [
                                    {
                                        "match": {
                                        "host.keyword": "thomson"
                                        }
                                    },
                                    {
                                        "match": {
                                        "ident": "%s"%(ident)
                                        }
                                    }
                                    ]
                                }
                                },
                                {
                                "bool": {
                                    "must": [
                                    {
                                        "match": {
                                        "ident.keyword": "Thomson-TOOL"
                                        }
                                    },
                                    {
                                        "match": {
                                        "message": "%s"%(self.ip)
                                        }
                                    }
                                    ]
                                }
                                },
                                {
                                "terms": {
                                    "ident.keyword": [
                                    "LiveStream"
                                    ]
                                }
                                }
                            ]
                            }
                        }
                        ]
                    }
                    }
                ],
                "filter": {
                    "range": {
                    "@timestamp": {
                        "gte": "now-%s"%(time),
                        "lte": "now"
                    }
                    }
                }
                }
            }
        }
        index = "logstash-%s"%(timesindex.replace('-','.'))
        elast = Elasticsearch([{'host':self.host, 'port': self.port}]).search(index= index,body = query,)
        # print query
        return elast['hits']['hits']

    def query_job_by_id(self, ident=None, time = "1y", size = 0, jid = None):
        """
        time: thoi gian loc log tu hien tai minute(m),hour(h), day(d)...
        Return array full log by ident
        """
        self.size = size if size else self.size
        query = {
            "sort": [{"@timestamp": "desc"}],
            "from": 0,
            "size": self.size,
            "_source": ["message"],
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "host.keyword": "thomson"
                            }
                        },
                        {
                            "match": {
                                "ident": "%s"%(ident)
                            }
                        },
                        {
                            "match": {
                                "message": ": %s,"%(jid)
                            }
                        }
                    ],
                    "filter": {
                        "range": {
                            "@timestamp": {
                                "gte": "now-%s"%(time),
                                "lte": "now"
                            }
                        }
                    }
                }
            }
        }
        elast = Elasticsearch([{'host':self.host, 'port': self.port}]).search(index= self.index, body = query,)
        # print query
        return elast['hits']['hits']

    def fiter_by_sev(self, ident=None, ip =0, lstSev=[], size = 0):
        """
        ip: ip addrss match
        lstSev: array severity
        """
        array = []
        for item in lstSev:
            array.append(item.lower())
        self.ip = ip if ip else self.ip
        query = {
            "sort": [{"@timestamp": "desc"}],
            "from": 0,
            "size": size if size else self.size,
            "_source": ["message"],
            "query": {
                "bool": {
                "must": [
                    {
                    "bool": {
                        "should": [
                        {
                            "bool": {
                            "should": [
                                {
                                "bool": {
                                    "must": [
                                    {
                                        "match": {
                                        "ident.keyword": "Monitor"
                                        }
                                    },
                                    {
                                        "match": {
                                        "message": "origin"
                                        }
                                    },
                                    {
                                        "match": {
                                        "message": "%s"%(ident)
                                        }
                                    }
                                    ]
                                }
                                },
                                {
                                "bool": {
                                    "must": [
                                    {
                                        "match": {
                                        "ident.keyword": "Monitor"
                                        }
                                    },
                                    {
                                        "match": {
                                        "message": "4500"
                                        }
                                    }
                                    ]
                                }
                                }
                            ]
                            }
                        },
                        {
                            "bool": {
                            "should": [
                                {
                                "bool": {
                                    "must": [
                                    {
                                        "match": {
                                        "host.keyword": "thomson"
                                        }
                                    },
                                    {
                                        "match": {
                                        "ident": "%s"%(ident)
                                        }
                                    }
                                    ]
                                }
                                },
                                {
                                "bool": {
                                    "must": [
                                    {
                                        "match": {
                                        "ident.keyword": "Thomson-TOOL"
                                        }
                                    },
                                    {
                                        "match": {
                                        "message": "%s"%(self.ip)
                                        }
                                    }
                                    ]
                                }
                                },
                                {
                                "terms": {
                                    "ident.keyword": [
                                    "LiveStream"
                                    ]
                                }
                                }
                            ]
                            }
                        }
                        ]
                    }
                    }
                ],
                "filter": {
                    "terms": {
                        "message": array
                    }
                }
                }
            }
        }
        elast = Elasticsearch([{'host':self.host, 'port': self.port}]).search(index= self.index, body = query,)
        return elast['hits']['hits']

    def check_ip(self,strIP):
        """
        check string is IP address
        return True/Flase
        """
        pattern = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        if pattern.findall(str(strIP)):
            return True
        else:
            return False

    def get_json_message(self,array):
        """"
        Return json from list message
        """
        result = [] #list message
        for item in array:
            tmp = item['_source']['message']
            try:
                mss = json.loads(tmp[tmp.index('{'):])
                result.append({'jid'            : int(mss['jid']if 'jid' in mss else 0),
                            'cat'           : mss['cat']if 'cat' in mss else '',
                            'lid'           : int(mss['lid']if 'lid' in mss else 0),
                            'res'           : mss['res']if 'res' in mss else '',
                            'jname'         : mss['jname']if 'jname' in mss else '',
                            'nid'           : mss['nid']if 'nid' in mss else '',
                            'sev'           : mss['sev']if 'sev' in mss else '',
                            'desc'          : ("%s %s")%(mss['desc']if 'desc' in mss else'', mss['host']if not self.check_ip(mss['host']) else''),
                            'opdate'        : mss['opdate']if 'opdate' in mss else '' ,
                            'cldate'        : mss['cldate']if 'cldate' in mss else''
                })
            except Exception as e:
                print e
        return json.dumps(result)
