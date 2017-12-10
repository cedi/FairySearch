#!/usr/bin/env python

import time
from os import path

def __save_server(ftp_server, host, port):
    """
    Saves the FTP Server with iths port associated to the ftp_server object

    :param ftp_server: the target object to which the host/port is saved
    :param host: the ftp server
    :param port: the port on which the ftp server is running
    """

    ports = set()
    if host in ftp_server:
        ports = ftp_server[host]
    else:
        ports = set()

    ports.add(port)
    ftp_server[host] = ports

def __save_files(file_list, host, files):
    """
    Stores the files associated to the server to the file_list object

    :param file_list: the target object to which the files are saved
    :param host: the ftp host
    :param files: the files found on the ftp server
    """
    for file_path in files:
        filename = path.basename(file_path) # TODO: get only the filename
        filename, extension = path.splitext(filename) # TODO: get only the extension
        filename_with_ext = filename + extension

        file_object = dict()

        if filename_with_ext in file_list:
            file_object = file_list[filename_with_ext]

        if "filename" not in file_object:
            file_object["filename"] = filename;

        if "extension" not in file_object:
            file_object["extension"] = extension

        # check if the server already exists in the object, if not create an
        # empty dict
        server = dict()

        if "server" in file_object:
            server = file_object["server"]

        # check if the server_host exists inside the server object, if not
        # create an empty dict
        server_host = dict()

        if host in server:
            host = server[host]

        # always set the path, so in case the file is moved we always have the
        # newest path
        server_host["path"] = file_path

        # always set the scan_date to now
        server_host["scan_date"] = time.time()

        # write the server_host back to the server dict
        server[host] = server_host

        # write the server dictionary back to the file_object
        file_object["server"] = server

        file_list[filename_with_ext] = file_object


def save_ftp_server(host, port, files):
    """
    Stores the host, port and files to the DB

    :param host: the ftp server
    :param port: the port
    :param files: files on the ftp server
    """

    # TODO: Replace with MongoDB Objects
    ftp_server = dict()
    file_list = dict()

    __save_server(ftp_server, host, port)
    print(ftp_server)

    __save_files(file_list, host, files)
    print(file_list)

if __name__ == "__main__":
    pass
