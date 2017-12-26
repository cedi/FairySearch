#!/usr/bin/env python

import sys
import os

import nmap
import ftp_walker
from util import eprint

def cb_open_port(host, port, port_info):
    """
    The callback 'cb_host' which is called for every found open port on a host

    Currently only supports port 21 for accessing ftp. May be improved in future
    in order to try each found port to access via ftp.

    :param host: The host to which belongs the open port
    :param port: The open port
    :param port_info: The nmap scan results for this port. currently unused.
    """
    print("## open port found: {0}:{1}".format(host, port))
    print('host: {0}, port: {1}, state : {2}'.format(host, port, port_info))

    if 21 == port:
        #ftp_walker.walk(host, port)
        print("FTP-Server: {0}".format(host))
    else:
        pass
        #eprint(" $$ Port {0} is currently not supported".format(port))


def cb_host(host, scan_result):
    """
    The callback for 'scan' which is called for each found host.

    Will itself run another nmap instance to scan for open ports on a specific
    host using nmap once again. For each found port it will then call a callback
    which tries to access the port via ftp.

    :param host: the ip address of the host
    :param scan_result: the can result in the following structure
        {'addresses': {'ipv4': '127.0.0.1'}, 'hostnames': [],
         'osmatch': [{'accuracy': '98',
                      'line': '36241',
                      'name': 'Juniper SA4000 SSL VPN gateway (IVE OS 7.0)',
                      'osclass': [{'accuracy': '98',
                                   'cpe': ['cpe:/h:juniper:sa4000',
                                           'cpe:/o:juniper:ive_os:7'],
                                   'osfamily': 'IVE OS',
                                   'osgen': '7.X',
                                   'type': 'firewall',
                                   'vendor': 'Juniper'}]},
                     {'accuracy': '91',
                      'line': '17374',
                      'name': 'Citrix Access Gateway VPN gateway',
                      'osclass': [{'accuracy': '91',
                                   'cpe': [],
                                   'osfamily': 'embedded',
                                   'osgen': None,
                                   'type': 'proxy server',
                                   'vendor': 'Citrix'}]}],
         'portused': [{'portid': '443', 'proto': 'tcp', 'state': 'open'},
                      {'portid': '113', 'proto': 'tcp', 'state': 'closed'}],
         'status': {'reason': 'syn-ack', 'state': 'up'},
         'tcp': {113: {'conf': '3',
                       'cpe': '',
                       'extrainfo': '',
                       'name': 'ident',
                       'product': '',
                       'reason': 'conn-refused',
                       'state': 'closed',
                       'version': ''},
                 443: {'conf': '10',
                       'cpe': '',
                       'extrainfo': '',
                       'name': 'http',
                       'product': 'Juniper SA2000 or SA4000 VPN gateway http config',
                       'reason': 'syn-ack',
                       'state': 'open',
                       'version': ''}},
         'vendor': {}}

    :return: 0 if everything has worked, != 0 to indicate an error
    """
    if scan_result['nmap']['scanstats']['uphosts'] == "0":
        return 1

    if scan_result['scan'][host]['status']['state'] != 'up':
        return 2

    # print('# Host "{0}" found, scanning for ports...'.format(host))

    try:
        nm = nmap.PortScanner() # instantiate nmap.PortScanner object
    except nmap.PortScannerError:
        eprint('Nmap not found', sys.exc_info()[0])
        return 3
    except:
        eprint("Unexpected error:", sys.exc_info()[0])
        return 4

    nm.scan(host, '1-443')
    for host in nm.all_hosts():
        if nm[host].state() != 'up':
            continue

        lport = list(nm[host].all_tcp())
        lport.sort()
        for port in lport:
            port_info = nm[host]['tcp'][port]
            if port_info['state'] == 'open':
                cb_open_port(host, port, port_info)

    return 0

def scan(network):
    """
    The network scanning function.
    Scans the network using 'nmap -sP'. For each found host there is a callback
    async called

    :param network: an ipaddress including it's subnetmask, eg. 192.168.0.0/24
    """
    nma = nmap.PortScannerAsync()
    nma.scan(hosts=network, arguments='-sP', callback=cb_host)

    while nma.still_scanning():
       nma.wait(2)

