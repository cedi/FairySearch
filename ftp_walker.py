#!/usr/bin/env python

import sys
import os

from ftplib import FTP

def walk_recursive(ftp, file_list, adir="."):
    """
    walkes recursively through the ftp file structure

    :param ftp: the FTP object
    :param file_list: a list which all files
    :param adir: the current working dir
    """
    subDirs = []
    gotdirs = []

    # change dir
    ftp.cwd(adir)

    # get current dir
    curdir = ftp.pwd()

    def cb_enumerate_files(ln):
        """
        callback function for ftp.retrlines('LIST')

        :param ln: the file list for the crawled folder
        """
        cols = ln.split(' ')
        objname = cols[len(cols)-1] # get name (same as awk '{print $8}'

        if ln.startswith('d'):
            subDirs.append(objname)
        else:
            file_list.append(os.path.join(curdir, objname)) # full path

    # get all dirs
    ftp.retrlines('LIST', cbEnumerateFiles)
    gotdirs = subDirs

    for subdir in gotdirs:
        recursiveFileList(ftp, file_list, subdir) # recurse

    # up after finishing everything
    ftp.cwd('..')

def walk_ftp_server(host, port=21):
    """
    Entry point for ftp_walker.
    Tries to connect to a server and then walks through all folders in order to
    crawl all existing files.

    :param host: the ftp host
    :param port: the port on which we try to connect. Currently not supported
    """
    print "### FTP Server is found: {0}:{1}".format(host, port)

    ftp = FTP(host)
    ftp.login()

    file_list = []
    walk_recursive(ftp, file_list)

    print(file_list)

