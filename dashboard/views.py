#coding: utf-8
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, HttpResponse
import logging
from dashboard import es

logger = logging.getLogger("default")


def index(request):
    return render_to_response('index.html')


def searchVp(request):
    dest = request.POST.get("dest", "*")
    viewpoint = request.POST.get("viewpoint", "*")
    query_string = "p_d_name: %s AND  name: %s" % (dest, viewpoint,)
    return HttpResponse(es.searchVp(query_string))


def getVpDetail(request):
    res = []
    vp_id = request.POST.get("vp_id")
    status = request.POST.get("status", "online")
    pin = es.getVpPin(vp_id)
    vps = es.getNearbyVp(pin)
    for vp in vps:
        vp["streams"] = es.getStreamlist(status,vp.get("vp_id"))
        res.append(vp)
    return HttpResponse(res)


def createStream(request):
    vp_id = request.POST.get("vp_id")
    user_id = request.POST.get("user_id")
    title = request.POST.get("title", "")
    st_id = es.createStream(vp_id,user_id, title)
    return HttpResponse({"stream_id": int(st_id)})


def getStream(request):
    st_id = request.POST.get("st_id")
    res = es.getStream(st_id)
    return HttpResponse(res)


def getStreamList(request):
    vp_id = request.POST.get("vp_id")
    status = request.POST.get("status", "online")
    return HttpResponse(es.getStreamlist(status, vp_id))
