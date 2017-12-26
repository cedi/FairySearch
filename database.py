#!/usr/bin/env python

import time
from os import path
from pymongo import MongoClient
import json

def __is_server_existing__(document, host, port):
    """
    Validates if a server with given host(url) and port is already existing in
    the document

    :param document: the document to check in
    :param host: the host which is searched inside the document
    :param port: the port which is searched inside the document
    """
    for server in document["server"]:
        if host == server["url"] and port == server["port"]:
            return True

    return False


def __save_server(ftp_server, host, port):
    """
    Saves the FTP Server with iths port associated to the ftp_server object

    :param ftp_server: the target object to which the host/port is saved
    :param host: the ftp server
    :param port: the port on which the ftp server is running
    """

    result = ftp_server.find({"host": host})
    if 0 < result.count():
        if port not in result[0]["ports"]:
            document = { "ports": port }
            ftp_server.update({ "host" : host}, { "$push": document } )
    else:
        document = { "host" : host, "ports" : [port] }
        ftp_server.insert(document)

def __save_files(file_list, host, port, files):
    """
    Stores the files associated to the server to the file_list object

    :param file_list: the target object to which the files are saved
    :param host: the ftp host
    :param files: the files found on the ftp server
    """
    for file_path in files:
        filename = path.basename(file_path)
        filename, extension = path.splitext(filename)

        result = file_list.find({ "filename": filename })

        if 0 < result.count():
            if __is_server_existing__(result[0], host, port):
                continue

            document = {
                "url" : host,
                "port": port,
                "extension" : extension,
                "path" : file_path,
                "scan_date" : time.time()
            }

            file_list.update({ "filename" : filename}, { "$push": { "server": document } } )
        else:
            document = {
                        "filename" : filename,
                        "server" : [
                            {
                                "url" : host,
                                "port": port,
                                "extension" : extension,
                                "path" : file_path,
                                "scan_date" : time.time()
                            }
                        ]
                    }
            file_list.insert(document)

def save_ftp_server(host, port, files):
    """
    Stores the host, port and files to the DB

    :param host: the ftp server
    :param port: the port
    :param files: files on the ftp server
    """

    # Connect to MongoDB and get the database
    mongo = MongoClient("mongodb://127.0.0.1:27019")
    db = mongo['metadata']

    # Get the base dictionaries, where i save the data
    ftp_server = db.ftp_server
    file_list = db.file_list

    __save_server(ftp_server, host, port)
    __save_files(file_list, host, port, files)

# Some testing code
if __name__ == "__main__":
    data_str = '{"1000GB.zip": {"filename": "1000GB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/1000GB.zip", "scan_date": 1512940989.0349853}}}, "100GB.zip": {"filename": "100GB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/100GB.zip", "scan_date": 1512940989.0350099}}}, "100KB.zip": {"filename": "100KB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/100KB.zip", "scan_date": 1512940989.0350497}}}, "100MB.zip": {"filename": "100MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/100MB.zip", "scan_date": 1512940989.0350645}}}, "10GB.zip": {"filename": "10GB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/10GB.zip", "scan_date": 1512940989.035082}}}, "10MB.zip": {"filename": "10MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/10MB.zip", "scan_date": 1512940989.0350947}}}, "1GB.zip": {"filename": "1GB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/1GB.zip", "scan_date": 1512940989.0351102}}}, "1KB.zip": {"filename": "1KB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/1KB.zip", "scan_date": 1512940989.0351198}}}, "1MB.zip": {"filename": "1MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/1MB.zip", "scan_date": 1512940989.0351331}}}, "200MB.zip": {"filename": "200MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/200MB.zip", "scan_date": 1512940989.0351427}}}, "20MB.zip": {"filename": "20MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/20MB.zip", "scan_date": 1512940989.035473}}}, "2MB.zip": {"filename": "2MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/2MB.zip", "scan_date": 1512940989.0354888}}}, "3MB.zip": {"filename": "3MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/3MB.zip", "scan_date": 1512940989.0354984}}}, "500MB.zip": {"filename": "500MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/500MB.zip", "scan_date": 1512940989.0355082}}}, "50MB.zip": {"filename": "50MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/50MB.zip", "scan_date": 1512940989.0355172}}}, "512KB.zip": {"filename": "512KB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/512KB.zip", "scan_date": 1512940989.035526}}}, "5MB.zip": {"filename": "5MB", "extension": ".zip", "server": {"90.130.70.73": {"path": "/5MB.zip", "scan_date": 1512940989.0355427}}}}'
    data = json.loads(data_str)

    save_ftp_server("1.2.3.4", 21, data)
    save_ftp_server("1.2.3.4", 31, data)
    save_ftp_server("4.5.6.7", 21, data)
