#!/usr/bin/env python

import os
import logging
import json
import time
from collections import defaultdict

logger = None

class G:
    fsname = None
    stats = defaultdict(lambda: defaultdict(int))

def read_lnet_stats(f):
    """
    expect input of a path to lnet stats
    return a dictionary with key/val pairs
    """
    ret = {'send_count': 0, 'recv_count': 0, 'send_length':0, 'recv_length': 0}

    pfile = os.path.normpath(f) + "/stats"
    with open(pfile, "r") as f:
            for line in f:
                chopped = line.split()
                if chopped[3]:
                    ret["send_count"] = int(chopped[3])
                if chopped[4]:
                    ret["recv_count"] = int(chopped[4])
                if chopped[7]:
                    ret["send_length"] = int(chopped[7])
		if chopped[8]:
		    ret["recv_length"] = int(chopped[8])	
    

    if ret['send_count'] == 0 and ret['recv_count'] == 0 and ret['send_length'] == 0 and ret['recv_length'] == 0 :
        return None

    return ret

def update():

        fpath = '/proc/sys/' + lnet
        ret = read_lnet_stats(fpath)
        if ret:
            G.stats[lnet] = ret

def metric_init(name, loglevel=logging.DEBUG):
    global logger
    logger = logging.getLogger("app.%s" % __name__)

def get_stats():

    if G.fsname is None:
        logger.error("No valid file system ... skip")
        return ""

    update()

    return json.dumps(G.stats)


def metric_cleanup():
    pass

if __name__ == '__main__':
    metric_init("lnet-stats")
    while True:
        print get_stats()
        time.sleep(5)
    metric_cleanup()

