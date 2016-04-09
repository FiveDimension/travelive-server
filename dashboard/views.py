#coding: utf-8
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponse
import logging
from dashboard import es
import json
from utils.view_helpers import HttpAjaxResponse

logger = logging.getLogger("default")


@csrf_exempt
def index(request):
    return render_to_response('index.html')


@csrf_exempt
def searchVp(request):
    param = json.loads(request.body)
    dest = param.get("dest", "*")
    viewpoint = param.get("viewpoint", "*")
    if not dest:
        dest = "*"
    if not viewpoint:
        viewpoint = "*"
    query_string = "p_d_name: %s AND  name: %s" % (dest, viewpoint)
    return HttpAjaxResponse(es.searchVp(query_string, False))


@csrf_exempt
def simpleSearchVp(request):
    param = json.loads(request.body)
    dest = param.get("dest", "*")
    viewpoint = param.get("viewpoint", "*")
    if not dest:
        dest = "*"
    if not viewpoint:
        viewpoint = "*"
    query_string = "p_d_name: %s AND  name: %s" % (dest, viewpoint)
    return HttpAjaxResponse(es.searchVp(query_string, True))


@csrf_exempt
def getVpDetail(request):
    res = []
    param = json.loads(request.body)
    vp_id = param.get("vp_id")
    status = param.get("status", "online")
    distance = param.get("distance", "5")
    if not status:
        status = "online"
    if not distance:
        distance = "5"
    pin = es.getVpPin(vp_id)
    vps = es.getNearbyVp(pin, distance)
    for vp in vps:
        vp["streams"] = es.getStreamlist(status,vp.get("vp_id"))
        res.append(vp)
    return HttpAjaxResponse(res)


@csrf_exempt
def createStream(request):
    param = json.loads(request.body)
    vp_id = param.get("vp_id")
    user_id = param.get("user_id")
    title = param.get("title", "")
    st_id = es.createStream(vp_id,user_id, title)
    return HttpAjaxResponse({"st_id": int(st_id)})


@csrf_exempt
def getStream(request):
    param = json.loads(request.body)
    st_id = param.get("st_id")
    res = es.getStream(st_id)
    return HttpAjaxResponse(res)


@csrf_exempt
def getStreamList(request):
    param = json.loads(request.body)
    vp_id = param.get("vp_id")
    status = param.get("status", "online")
    if not status:
        status = "online"
    return HttpAjaxResponse(es.getStreamlist(status, vp_id))


@csrf_exempt
def deleteStream(request):
    param = json.loads(request.body)
    st_id = param.get("st_id")
    return HttpAjaxResponse(es.deleteStream(st_id))


@csrf_exempt
def doFavorite(request):
    param = json.loads(request.body)
    # user_id = param.get("user_id")
    st_id = param.get("st_id")
    res = es.doFavoriteStream(st_id)
    return HttpAjaxResponse({"message": True})


@csrf_exempt
def addUser(request):
    param = json.loads(request.body)
    username = param.get("username")
    password = param.get("password", "")
    return HttpAjaxResponse(es.addUser(username, password))


@csrf_exempt
def login(request):
    param = json.loads(request.body)
    username = param.get("username")
    user_id = es.getUser(username)
    if user_id:
        return HttpAjaxResponse({"message": True, "user_id": user_id})
    else:
        return HttpAjaxResponse({"message": False})


@csrf_exempt
def addRoute(request):
    param = json.loads(request.body)
    user_id = param.get("user_id")
