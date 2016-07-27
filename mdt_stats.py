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
    mdtnames = None
    stats = defaultdict(lambda: defaultdict(int))

def read_mdt_stats(f):
    """
    expect input of a path to ost stats
    return a dictionary with key/val pairs
    """
    ret = {'read_bytes_sum': 0, 'write_bytes_sum': 0}
    f1 = f
    pfile = os.path.normpath(f) + "/md_stats"
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
                chopped = line.split('=');
                if "kbytesavail" in chopped[0]:
                        ret["kbytes_avail"] = int(chopped[0])

    if ret['read_bytes_sum'] == 0 and ret['write_bytes_sum'] == 0:
        return None

def update():

    for mdt in G.mdtnames:
        fpath = '/proc/fs/lustre/mdt/' + mdt
        ret = read_mdt_stats(fpath)
        if ret:
            G.stats[mdt] = ret

def metric_init(name, loglevel=logging.DEBUG):
    global logger
    logger = logging.getLogger("app.%s" % __name__)
    G.fsname, G.mdtnames = lfs_utils.scan_mdts()

def get_stats():

    if G.fsname is None:
        logger.error("No valid file system ... skip")
        return ""

    update()

    return json.dumps(G.stats)


def metric_cleanup():
    pass

if __name__ == '__main__':
    metric_init("mdt-stats")
    while True:
        print get_stats()
        time.sleep(5)
    metric_cleanup()

