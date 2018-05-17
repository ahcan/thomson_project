import requests
import json
import time
from elasticsearch import Elasticsearch
uri = "http://183.80.133.166:9100"
qbody = {
    "query":{
        "match_all":{}
    }
}
elst = Elasticsearch([{'host':'118.69.190.70','prot':9200}])
r= elst.search(index='_all',body={
    "sort":[{
        "@timestamp": "desc"
    }],
    "size":20,
    "query":{
        "match":{"ident.keyword": "Thomson-HNI"}
    }
})
print  r['hits']['hits']