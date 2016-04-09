__author__ = 'jian.zhang'

from sysconf.settings import *
from utils.random import create_id
import requests,json


def searchVp(query_string):
    res = []
    url = ES_HOST + "/" + INDEX + "/" + VIEWPOINT_TYPE + "/_search"
    data = {
      "query": {
        "query_string": {
          "query": query_string
        }
      },
      "size": 20
    }

    r = requests.post(url, data=json.dumps(data))
    hits = r.json()["hits"]["hits"]
    for hit in hits:
        res.append(hit["_source"])
    return res


def getVpPin(vp_id):
    url = ES_HOST + "/" + INDEX + "/" + VIEWPOINT_TYPE + "/" +"vp_"+ str(vp_id)
    r = requests.get(url)
    return r.json()["_source"]["pin"]["location"]


def getNearbyVp(pin):
    res = []
    url = ES_HOST + "/" + INDEX + "/" + VIEWPOINT_TYPE + "/_search"
    data = {
      "query": {
        "filtered": {
          "filter": {
            "geo_distance": {
              "distance": "8km",
              "pin.location": pin
            }
          }
        }
      }
    }

    r = requests.post(url, data=json.dumps(data))
    hits = r.json()["hits"]["hits"]
    for hit in hits:
        res.append(hit["_source"])
    return res


def createStream(vp_id, user_id, title):
    st_id = create_id(user_id)
    url = ES_HOST + "/" + INDEX + "/" + STREAM_TYPE + "/" + st_id
    data = {
        "st_id": st_id,
        "status": "online",
        "p_vp_id": vp_id,
        "p_user_id": user_id,
        "favorites_count": 0,
        "title": title,
    }
    r = requests.post(url, data=json.dumps(data))
    return st_id


def getStream(st_id):
    url = ES_HOST + "/" + INDEX + "/" + STREAM_TYPE + "/" + str(st_id)
    r = requests.get(url)
    return r.json()["_source"]


def getStreamlist(status, vp_id):
    res = []
    url = ES_HOST + "/" + INDEX + "/" + STREAM_TYPE + "/_search"
    data = {
          "query": {
            "filtered": {
              "filter": {
                "bool": {
                  "must": [
                    {
                      "query": {
                        "query_string": {
                          "query": "status: %s AND p_vp_id: %s" % (status, str(vp_id))
                        }
                      }
                    }
                  ]
                }
              }
            }
          },
          "size": 20
        }

    r = requests.post(url, data=json.dumps(data))
    hits = r.json()["hits"]["hits"]
    for hit in hits:
        res.append(hit["_source"])
    return res






