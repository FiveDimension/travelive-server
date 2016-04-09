__author__ = 'jian.zhang'

from sysconf.settings import *
from utils import util
import requests,json

AMAP_URL = "http://restapi.amap.com/v3/direction/walking?origin=%s&destination=%s&key=388711e45bb17d065a21a32cdd8b4d49"


def getDirection(location1, location2):
    url = AMAP_URL % (str(location1["lon"])+","+str(location1["lat"]), str(location2["lon"])+","+str(location2["lat"]))
    r = requests.get(url)
    duration = r.json()["route"]["paths"][0]["duration"]
    return int(duration)