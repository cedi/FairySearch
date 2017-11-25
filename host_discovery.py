#!/usr/bin/env python

import sys
import os

import nmap

# Data structure looks like :
#
#      {'addresses': {'ipv4': '127.0.0.1'},
#       'hostnames': [],
#       'osmatch': [{'accuracy': '98',
#                    'line': '36241',
#                    'name': 'Juniper SA4000 SSL VPN gateway (IVE OS 7.0)',
#                    'osclass': [{'accuracy': '98',
#                                 'cpe': ['cpe:/h:juniper:sa4000',
#                                         'cpe:/o:juniper:ive_os:7'],
#                                 'osfamily': 'IVE OS',
#                                 'osgen': '7.X',
#                                 'type': 'firewall',
#                                 'vendor': 'Juniper'}]},
#                   {'accuracy': '91',
#                    'line': '17374',
#                    'name': 'Citrix Access Gateway VPN gateway',
#                    'osclass': [{'accuracy': '91',
#                                 'cpe': [],
#                                 'osfamily': 'embedded',
#                                 'osgen': None,
#                                 'type': 'proxy server',
#                                 'vendor': 'Citrix'}]}],
#       'portused': [{'portid': '443', 'proto': 'tcp', 'state': 'open'},
#                    {'portid': '113', 'proto': 'tcp', 'state': 'closed'}],
#       'status': {'reason': 'syn-ack', 'state': 'up'},
#       'tcp': {113: {'conf': '3',
#                     'cpe': '',
#                     'extrainfo': '',
#                     'name': 'ident',
#                     'product': '',
#                     'reason': 'conn-refused',
#                     'state': 'closed',
#                     'version': ''},
#               443: {'conf': '10',
#                     'cpe': '',
#                     'extrainfo': '',
#                     'name': 'http',
#                     'product': 'Juniper SA2000 or SA4000 VPN gateway http config',
#                     'reason': 'syn-ack',
#                     'state': 'open',
#                     'version': ''}},
#       'vendor': {}}

def cbFoundOpenPort(host, port, port_info):
    print "## open port found: {0}:{1}".format(host, port)
    print('host: {0}, port: {1}, state : {2}'.format(host, port, port_info))

    if port == "21":
        scanFTP(host, port)

    print " $$ Port {0} is currently not supported".format(port)


def cbHostUp(host, scan_result):
    if scan_result['nmap']['scanstats']['uphosts'] == "0":
        return

    if scan_result['scan'][host]['status']['state'] != 'up':
        return

    print '# Host "{0}" found, scanning for ports...'.format(host)

    try:
        nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
    except nmap.PortScannerError:
        print('Nmap not found', sys.exc_info()[0])
        sys.exit(1)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(1)

    nm.scan(host, '1-443')
    for host in nm.all_hosts():
        if nm[host].state() != 'up':
            continue

        lport = list(nm[host].all_tcp())
        lport.sort()
        for port in lport:
            port_info = nm[host]['tcp'][port]
            if port_info['state'] == 'open':
                cbFoundOpenPort(host, port, port_info)

def scanNetwork(network):
    nma = nmap.PortScannerAsync()
    nma.scan(hosts=network, arguments='-sP', callback=cbHostUp)

    while nma.still_scanning():
       nma.wait(2)

