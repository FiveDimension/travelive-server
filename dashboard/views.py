#coding: utf-8
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, HttpResponse
import logging
from dashboard import es
import json
from utils.view_helpers import HttpAjaxResponse

logger = logging.getLogger("default")


def index(request):
    return render_to_response('index.html')


def searchVp(request):
    param = json.loads(request.body)
    dest = param.get("dest", "*")
    viewpoint = param.get("viewpoint", "*")
    if not dest:
        dest = "*"
    if not viewpoint:
        viewpoint = "*"
    query_string = "p_d_name: %s AND  name: %s" % (dest, viewpoint)
    return HttpAjaxResponse(es.searchVp(query_string))


def getVpDetail(request):
    res = []
    param = json.loads(request.body)
    vp_id = param.get("vp_id")
    status = param.get("status", "online")
    if not status:
        status = "online"
    pin = es.getVpPin(vp_id)
    vps = es.getNearbyVp(pin)
    for vp in vps:
        vp["streams"] = es.getStreamlist(status,vp.get("vp_id"))
        res.append(vp)
    return HttpAjaxResponse(res)


def createStream(request):
    param = json.loads(request.body)
    vp_id = param.get("vp_id")
    user_id = param.get("user_id")
    title = param.get("title", "")
    st_id = es.createStream(vp_id,user_id, title)
    return HttpAjaxResponse({"st_id": int(st_id)})


def getStream(request):
    param = json.loads(request.body)
    st_id = param.get("st_id")
    res = es.getStream(st_id)
    return HttpAjaxResponse(res)


def getStreamList(request):
    param = json.loads(request.body)
    vp_id = param.get("vp_id")
    status = param.get("status", "online")
    if not status:
        status = "online"
    return HttpAjaxResponse(es.getStreamlist(status, vp_id))
