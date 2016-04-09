#coding: utf-8
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
import logging
logger = logging.getLogger("default")

def index(request):
    return render_to_response('index.html')
