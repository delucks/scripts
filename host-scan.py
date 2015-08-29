#!/usr/bin/python3
import socket
import ipaddress
import json
import time
import random
import argparse

'''
host-scan.py
    this script serially queries the default DNS 
    server for IP address mappings in a subnet,
    then returns the results in JSON
author: delucks

Only use on systems you have authorization to query,
and set reasonable delay for politeness.
'''

p = argparse.ArgumentParser(description='scan a subnet for hostnames')
p.add_argument('subnet', help='the subnet you\'d like to scan, in CIDR notation')
p.add_argument('-d', '--delay', help='delay between serial DNS requests', default=10, type=int)
p.add_argument('-o', '--outfile', help='output results in JSON to this file', default='results.json')
p.add_argument('-p', '--public', help='allow scanning public IP space (USE AT YOUR OWN RISK)', action='store_true')
p.add_argument('-r', '--randomize', help='randomize (0, delay)', action='store_true')
args = p.parse_args()

print('Preprocessing: {}'.format(args.subnet))

subnet = ipaddress.ip_network(args.subnet)

# prompt user for politeness

if not subnet.is_private and not args.public:
    print('[WARNING] Specified subnet is public address space. If this is intentional, run with -p')
    socket.sys.exit(1)

if args.delay < 10:
    print('[WARNING] Specified request delay is fairly fast, be polite!')

def trawl_range(host_range, delay_max, delay_israndom):
    name_lookups = {}
    for ip_addr in host_range:
        ip = str(ip_addr)
        try:
            # name, aliases, ips = socket.gethostbyaddr(ip_addr)
            host_struct = socket.gethostbyaddr(ip)
        except socket.herror:
            print('{}: No host records'.format(ip))
            continue
        ip_info = {
                'name': host_struct[0],
                'aliases': host_struct[1],
                'other_ips': host_struct[2]
        }
        name_lookups[ip] = ip_info
        if delay_israndom:
            wait_amt = random.randint(0, delay_max)
        else:
            wait_amt = delay_max
        print('{}: {} (waiting {} seconds)'.format(ip, host_struct[0], wait_amt))
        time.sleep(wait_amt)
    return name_lookups

lookups = trawl_range(subnet.hosts(), args.delay, args.randomize)

with open(args.outfile,'w') as f:
    f.write(json.dumps(lookups))
