__author__ = 'jian.zhang'

import time
import hashlib
import sys
import copy

def create_id(user_id):
    return str(user_id) + str(int(time.time()))


def get_hash(username):
    return int(hashlib.sha1(username).hexdigest(), 16) % (10 ** 8)


def getMM(list):
    res = []
    for i in list:
        for j in list:
            if i != j and not (j, i) in res:
                res.append((i, j))
    return res


def getAllPath(vp_id_list, all_conn):
    for i in copy.deepcopy(all_conn):
        temp = i["vp_start"]
        i["vp_start"] = i["vp_end"]
        i["vp_end"] = temp
        all_conn.append(i)
    allPath = []
    for vp_id in vp_id_list:
        vps = []
        durations = []
        for i in xrange(len(vp_id_list)):
            vp_id,min_duration,vps = getOnePath(vp_id, all_conn, vps)
            durations.append(min_duration)
        allPath.append((vps, durations))
    return allPath


def getOnePath(vp_id, all_conn, vps):
    min_duration = sys.maxint
    next_vp_id = None
    # duration = None
    for a in all_conn:
        if a["vp_start"] == vp_id:
            if a["duration"] < min_duration and not a["vp_end"] in vps:
                next_vp_id = a["vp_end"]
                min_duration = a["duration"]
    vps.append(vp_id)
    return next_vp_id, min_duration,vps

all_conn = [{'duration': 1388, 'vp_start': 1, 'vp_end': 2},
            {'duration': 457, 'vp_start': 1, 'vp_end': 3},
            {'duration': 7053, 'vp_start': 1, 'vp_end': 4},
            {'duration': 4408, 'vp_start': 1, 'vp_end': 5},
            {'duration': 1492, 'vp_start': 2, 'vp_end': 3},
            {'duration': 6716, 'vp_start': 2, 'vp_end': 4},
            {'duration': 4626, 'vp_start': 2, 'vp_end': 5},
            {'duration': 6943, 'vp_start': 3, 'vp_end': 4},
            {'duration': 4866, 'vp_start': 3, 'vp_end': 5},
            {'duration': 11461, 'vp_start': 4, 'vp_end': 5}]

if __name__ == "__main__":
    for i in copy.deepcopy(all_conn):
        temp = i["vp_start"]
        i["vp_start"] = i["vp_end"]
        i["vp_end"] = temp
        all_conn.append(i)
    print(all_conn)
    res = getAllPath([1, 2, 3, 4, 5],all_conn)
    print res

