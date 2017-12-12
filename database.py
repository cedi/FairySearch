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
        filename = path.basename(file_path)
        filename, extension = path.splitext(filename)
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
            server_host = server[host]

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
    import json

    data_str = '{"1000GB.zip": {"filename": "1000GB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/1000GB.zip", "scan_date": 1512940989.0349853}}}, "100GB.zip": {"filename": "100GB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/100GB.zip", "scan_date": 1512940989.0350099}}}, "100KB.zip": {"filename": "100KB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/100KB.zip", "scan_date": 1512940989.0350497}}}, "100MB.zip": {"filename": "100MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/100MB.zip", "scan_date": 1512940989.0350645}}}, "10GB.zip": {"filename": "10GB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/10GB.zip", "scan_date": 1512940989.035082}}}, "10MB.zip": {"filename": "10MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/10MB.zip", "scan_date": 1512940989.0350947}}}, "1GB.zip": {"filename": "1GB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/1GB.zip", "scan_date": 1512940989.0351102}}}, "1KB.zip": {"filename": "1KB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/1KB.zip", "scan_date": 1512940989.0351198}}}, "1MB.zip": {"filename": "1MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/1MB.zip", "scan_date": 1512940989.0351331}}}, "200MB.zip": {"filename": "200MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/200MB.zip", "scan_date": 1512940989.0351427}}}, "20MB.zip": {"filename": "20MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/20MB.zip", "scan_date": 1512940989.035473}}}, "2MB.zip": {"filename": "2MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/2MB.zip", "scan_date": 1512940989.0354888}}}, "3MB.zip": {"filename": "3MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/3MB.zip", "scan_date": 1512940989.0354984}}}, "500MB.zip": {"filename": "500MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/500MB.zip", "scan_date": 1512940989.0355082}}}, "50MB.zip": {"filename": "50MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/50MB.zip", "scan_date": 1512940989.0355172}}}, "512KB.zip": {"filename": "512KB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/512KB.zip", "scan_date": 1512940989.035526}}}, "5MB.zip": {"filename": "5MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/5MB.zip", "scan_date": 1512940989.0355427}}}}' 
    data = json.loads(data_str)

    save_ftp_server("1.2.3.4", 21, data)
