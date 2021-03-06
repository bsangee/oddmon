#!/usr/bin/env python

import os
import logging
import json
import time
from collections import defaultdict
try:
    from oddmon import lfs_utils
except:
    import lfs_utils

logger = None

class G:
    fsname = None
    ostnames = None
    stats = defaultdict(lambda: defaultdict(int))

def read_ost_stats(f):
    """
    expect input of a path to ost stats
    return a dictionary with key/val pairs
    """
    ret = {'read_bytes_sum': 0, 'write_bytes_sum': 0}
    f1 = f	
    f2 = f
    pfile = os.path.normpath(f) + "/stats"
    with open(pfile, "r") as f:
            for line in f:
                chopped = line.split()
                if chopped[0] == "snapshot_time":
                    ret["snapshot_time"] = chopped[1]
                if chopped[0] == "write_bytes":
                    ret["write_bytes_sum"] = int(chopped[6])
                if chopped[0] == "read_bytes":
                    ret["read_bytes_sum"] = int(chopped[6])
    
    pfile = os.path.normpath(f1) + "/kbytesavail"
    with open(pfile, "r") as f1:
	    for line in f1:
			ret["kbytes_avail"] = int(line)	
    
    pfile = os.path.normpath(f2) + "/job_stats"
    with open(pfile, "r") as f2:
            for line in f2:
                chopped = line.split(":")
                if chopped[0] == "job_stats":
                        ret["job_stats"] = chopped[1]			

    if ret['read_bytes_sum'] == 0 and ret['write_bytes_sum'] == 0:
        return None

    return ret

def update():

    for ost in G.ostnames:
        fpath = '/proc/fs/lustre/obdfilter/' + ost
        ret = read_ost_stats(fpath)
        if ret:
            G.stats[ost] = ret

def metric_init(name, loglevel=logging.DEBUG):
    global logger
    logger = logging.getLogger("app.%s" % __name__)
    G.fsname, G.ostnames = lfs_utils.scan_osts()

def get_stats():

    if G.fsname is None:
        logger.error("No valid file system ... skip")
        return ""

    update()

    return json.dumps(G.stats)


def metric_cleanup():
    pass

if __name__ == '__main__':
    metric_init("ost-stats")
    while True:
        print get_stats()
        time.sleep(5)
    metric_cleanup()

