#!/usr/bin/env python

import os
import logging
import json
import time
import subprocess
from collections import defaultdict

logger = None

class G:
    stats = defaultdict(lambda: defaultdict(int))

def read_oss_stats():
    ret = {'cpu': 0, 'mem': 0}
    count=1
    cmd = subprocess.Popen('sar 1 1 -r -u', shell=True, stdout=subprocess.PIPE)
    for line in cmd.stdout:	
                chopped = line.split()
		if chopped and count == 10:
		   ret['cpu'] = 100 - int(chopped[-1]);
		if chopped and count == 13:
		   ret['mem'] = int(chopped[3]);			
		count = count+1; 	


    return ret

def update():

        ret = read_oss_stats()
        if ret:
            G.stats = ret

def metric_init(name, loglevel=logging.DEBUG):
    global logger
    logger = logging.getLogger("app.%s" % __name__)

def get_stats():


    update()

    return json.dumps(G.stats)


def metric_cleanup():
    pass

if __name__ == '__main__':
    metric_init("oss-stats")
    while True:
        print get_stats()
        time.sleep(5)
    metric_cleanup()

