#!/usr/bin/env python

import os
import glob
import logging

class G:
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def scan_osts():
    fsname = None
    ostnames = []
    osts = glob.glob("/proc/fs/lustre/obdfilter/*OST*")
    if len(osts) != 0:
        fsname, _ = os.path.basename(osts[0]).split("-")
        for ost in osts:
            ostnames.append(os.path.basename(ost))
    return fsname, ostnames

def scan_mdts():
    fsname = None
    mdtnames = []
    mdts = glob.glob("/proc/fs/lustre/mdt/*MDT*")
    if len(mdts) != 0:
        fsname, _ = os.path.basename(mdts[0]).split("-")
        for mdt in mdts:
            mdtnames.append(os.path.basename(mdt))
    return fsname, mdtnames


def get_filehandler(f, m="w", level=logging.DEBUG):
    fh = logging.FileHandler(filename=f, mode=m)
    fh.setLevel(level)
    fh.setFormatter(G.fmt)
    return fh

def get_consolehandler(level=logging.DEBUG):
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(G.fmt)
    return ch



