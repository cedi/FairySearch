#!/usr/bin/env python

import sys
import os

from ftplib import FTP

def walk_recursive(ftp, myFiles, adir="."):
    subDirs = []
    gotdirs = []

    # change dir
    ftp.cwd(adir)

    # get current dir
    curdir = ftp.pwd()

    def cb_enumerate_files(ln):
        """
        callback functino for ftp.retrlines('LIST')
        """
        cols = ln.split(' ')
        objname = cols[len(cols)-1] # get name (same as awk '{print $8}'

        if ln.startswith('d'):
            subDirs.append(objname)
        else:
            myFiles.append(os.path.join(curdir, objname)) # full path

    # get all dirs
    ftp.retrlines('LIST', cbEnumerateFiles)
    gotdirs = subDirs

    for subdir in gotdirs:
        recursiveFileList(ftp, myFiles, subdir) # recurse

    ftp.cwd('..') # up after finishing everything

def walk_ftp_server(host, port=21):
    print "### FTP Server is found: {0}:{1}".format(host, port)
    ftp = FTP(host)
    ftp.login()

    myFiles = []
    walk_recursive(ftp, myFiles)

    print(myFiles)

