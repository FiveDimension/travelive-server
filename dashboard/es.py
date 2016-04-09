__author__ = 'jian.zhang'

from sysconf.settings import *
from utils import util
import requests,json


def searchVp(query_string, isSimple):
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
        if isSimple:
            res.append(hit["_source"]["name"])
        else:
            res.append(hit["_source"])
    return res


def getVpPin(vp_id):
    url = ES_HOST + "/" + INDEX + "/" + VIEWPOINT_TYPE + "/" +"vp_"+ str(vp_id)
    r = requests.get(url)
    return r.json()["_source"]["pin"]["location"]


def getNearbyVp(pin, distance):
    res = []
    url = ES_HOST + "/" + INDEX + "/" + VIEWPOINT_TYPE + "/_search"
    data = {
      "query": {
        "filtered": {
          "filter": {
            "geo_distance": {
              "distance": str(distance) + "km",
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
    st_id = util.create_id(user_id)
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


def doFavoriteStream(st_id):
    source = getStream(st_id)
    url = ES_HOST + "/" + INDEX + "/" + STREAM_TYPE + "/" + str(st_id)
    source["favorites_count"] += 1
    r = requests.post(url, data=json.dumps(source))
    return True


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


def deleteStream(st_id):
    url = ES_HOST + "/" + INDEX + "/" + STREAM_TYPE + "/" + str(st_id)
    r = requests.delete(url)
    return {"message": True}


def addUser(username, password):
    id = util.get_hash(username)
    url = ES_HOST + "/" + INDEX + "/" + USER_TYPE + "/%d" % (id,)
    data = {
        "user_id": id,
        "username": username,
        "password": password,
    }
    r = requests.post(url, data=json.dumps(data))
    return {"message": True, "user_id": id}


def getUser(username):
    url = ES_HOST + "/" + INDEX + "/" + USER_TYPE + "/_search"
    data = {
      "query": {
        "query_string": {
          "query": "username: "+username
        }
      },
      "size": 1
    }
    r = requests.post(url, data=json.dumps(data))
    hits = r.json()["hits"]["hits"]

    if hits:
        return hits[0]["_source"]["user_id"]
