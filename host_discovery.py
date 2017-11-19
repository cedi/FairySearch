#!/usr/bin/env python

import sys
import os

import nmap                         # import nmap.py module
try:
    nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(1)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(1)


# Data structure looks like :
#
#      {'addresses': {'ipv4': '192.168.43.34'},
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



#nm.scan('192.168.43.34', '22-443')      # scan host 192.168.43.34, ports from 22 to 443
#nm.command_line()                   # get command line used for the scan : nmap -oX - -p 22-443 192.168.43.34
#nm.scaninfo()                       # get nmap scan informations {'tcp': {'services': '22-443', 'method': 'connect'}}
#nm.all_hosts()                      # get all hosts that were scanned
#nm['192.168.43.34'].hostname()          # get one hostname for host 192.168.43.34, usualy the user record
#nm['192.168.43.34'].hostnames()         # get list of hostnames for host 192.168.43.34 as a list of dict [{'name':'hostname1', 'type':'PTR'}, {'name':'hostname2', 'type':'user'}]
#nm['192.168.43.34'].state()             # get state of host 192.168.43.34 (up|down|unknown|skipped) 
#nm['192.168.43.34'].all_protocols()     # get all scanned protocols ['tcp', 'udp'] in (ip|tcp|udp|sctp)
#if ('tcp' in nm['192.168.43.34']):
#    list(nm['192.168.43.34']['tcp'].keys()) # get all ports for tcp protocol
#
#nm['192.168.43.34'].all_tcp()           # get all ports for tcp protocol (sorted version)
#nm['192.168.43.34'].all_udp()           # get all ports for udp protocol (sorted version)
#nm['192.168.43.34'].all_ip()            # get all ports for ip protocol (sorted version)
#nm['192.168.43.34'].all_sctp()          # get all ports for sctp protocol (sorted version)
#if nm['192.168.43.34'].has_tcp(22):     # is there any information for port 22/tcp on host 192.168.43.34
#    nm['192.168.43.34']['tcp'][22]          # get infos about port 22 in tcp on host 192.168.43.34
#    nm['192.168.43.34'].tcp(22)             # get infos about port 22 in tcp on host 192.168.43.34
#    nm['192.168.43.34']['tcp'][22]['state'] # get state of port 22/tcp on host 192.168.43.34 (open
#
#
## a more usefull example :
#for host in nm.all_hosts():
#    print('----------------------------------------------------')
#    print('Host : {0} ({1})'.format(host, nm[host].hostname()))
#    print('State : {0}'.format(nm[host].state()))
#
#    for proto in nm[host].all_protocols():
#        print('----------')
#        print('Protocol : {0}'.format(proto))
#
#        lport = list(nm[host][proto].keys())
#        lport.sort()
#        for port in lport:
#            print('port : {0}\tstate : {1}'.format(port, nm[host][proto][port]))
#
#print('----------------------------------------------------')

nma = nmap.PortScannerAsync()

def callback_result(host, results):
    """
    Async Callback per host

    This handler will process the scan results per host

    :param host: the ip address fo the scanned host 
    :param results: the scan result as a dictionary

    :returns: nothing
    """

    scan_results = results['scan']

    # check the scan results if a host is up, then procceed
    for host in scan_results:
        scan_result = scan_results[host]

        # get the host state (if it's up or if it's down
        host_status = scan_result['status']['state']

        # if the host state is up
        if host_status == "up":
            print "host: %s , status: %s" % (host, host_status)


# Scan the specified subnet

# ~~~~~~~~ TODO ~~~~~~~~
# create a patch for the Async Callback, to specify an additional parameter
# thats passed to the callback every time a callback is called.
# This could be used for eg. a additional callback that's called from within
# the callback. I need this for more async handling of a scan result for eg.
# when a scanned host is up, to move all those functionality into another
# separated function
# ~~~~~~~~ / ~~~~~~~~
nma.scan(hosts='127.0.0.1', arguments='-sP', callback=callback_result)

# wait until all async scanns are done
nma.wait()

