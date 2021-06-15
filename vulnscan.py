#!/bin/python3

""" This is a script I developed to automate the retrievval of network information and
    then calculate the network address and CIDR range of the local network.  I have not 
    tested it extensively on subnetted networks but it should work on them aswell.
    It then calls a bash script 'vulnscan.sh' which performs an nmap scan.  The specifics 
    of that scan are described in that script. NOTE: of the below modules 'netaddr.py' and
    'bcolors.py' are local modules and need to be located in the same directory as 'vulnscan.py',
    netifaces is not in the default python modules and needs to be installed using
    'pip install netifaces'.  Additionally a directory named saved_nmap_scans will need
    to be created and 'vulnscan.sh' needs to be in the directory """

import netifaces                    # a module for retrieving network information
import netaddr as n                 # contains functions I created to run the script (local)
import subprocess                   # following two modules are for calling the bash script 
import shlex                        # and sending it the necessary variables values
from bcolors import bcolors as b    # just to add some color (local)
from sys import exit                # to break out of the script
import getpass                      # to get the username
import pyfiglet                     # to create an ascii banner

username = getpass.getuser()        # gets the username for use at the end of 'vulnscan.sh'

""" (1) This section uses the netifaces module to retrieve network addresses """

get_default = netifaces.gateways()             
client_gateway = get_default['default'][2][1]   
ip_addrs = {}                                   
ip_addrs = netifaces.ifaddresses(client_gateway)
host = ip_addrs[2][0]['addr']
netmask = ip_addrs[2][0]['netmask']             
broadcast = ip_addrs[2][0]['broadcast']

""" (2) This section splits an IPv4 address on the '.' and places the octets in the 'broadcast/netmask_octets_list'. 
    It then calls the 'get_split_binary_list()' function, which converts a list of IPv4 octets to a list of binary 
    equivalents for the broadcast addr and the netmask. """

broadcast_split_binary_list = n.get_split_binary_list(broadcast) 
netmask_split_binary_list = n.get_split_binary_list(netmask)

""" (4) This section calls the 'adding()' function which takes the arguements from the 'get_split_binary_list()' function
    and creates the binary equivalent of the network address. """

network_id_list = n.anding(broadcast_split_binary_list, netmask_split_binary_list)

""" (6) This section uses the 'netmask_octets_list' and calls the 'cidr_calculator()'function to calculate the CIDR 
    range of the network address. """

CIDR = n.cidr_calculator(netmask)

""" (8) This section the list of binary digits, 'network_id_list', from the 'anding()' 
    function and passes it into the 'get_net_addr()' function."""

net_addr, octets_dict, net_addr_no_CIDR, gateway = n.get_net_addr(network_id_list, CIDR)

""" This creates a banner. """
try:
    banner = pyfiglet.figlet_format("scanBuilder")
    print(f"\n{b.OKBLUE}{b.BOLD}{banner}{b.ENDC}")
except ModuleNotFoundError:
    pass

print(f"\t{b.OKBLUE}{b.BOLD}Get Net Info & Scan Your Network{b.ENDC}")
print(f"\n{b.BOLD}{b.CGREY}Cyber{b.OKBLUE}IQ{b.WARNING}.{b.OKBLUE}ai, {b.ENDC}Powered by Vulners")

print(f"\n{b.WARNING}This scan is intended for scanning your internal network, from a quick scan to an indepth vulnerability scan")

""" (10) This section prints out the results """

print(f"\n{b.OKGREEN}The IP address of your computer is: {b.ENDC}{b.BOLD}{host}{b.ENDC}")
print(f"{b.OKGREEN}The network netmask is: {b.ENDC}{b.BOLD}{netmask}{b.ENDC}")
print(f"{b.OKGREEN}The broadcast address is: {b.ENDC}{b.BOLD}{broadcast}{b.ENDC}")
print(f"{b.OKGREEN}The gateway address is: {b.ENDC}{b.BOLD}{gateway}{b.ENDC}")
print(f"{b.OKGREEN}The network CIDR range is: {b.ENDC}{b.BOLD}{CIDR}{b.ENDC}")

""" (11)This line asks the user if they want to use the network address generated from
    the above script asking for a 'y', 'n' or 'q' and storing the value in the 'choice1' variable"""
print(f"\n{b.OKGREEN}The network address is: {b.ENDC}{b.BOLD}{net_addr}{b.ENDC}") 
choice1 = input(f"Do you want contine to scan? {b.WARNING}('y' or 'q' to quit){b.ENDC}\n(default=y)>> ") or "y"

while True:
    # (option 1)
    if choice1.lower() == 'y':
        subprocess.call(shlex.split(f"sudo ./scan_builder2.sh {net_addr} {username}"))
        exit()
        break
     
    elif choice1.lower() == 'q':
        exit()
    # (invalid input)
    else:
        choice1 = input(f"\n\t{b.FAIL}(Invalid input)\n\n{b.ENDC}Please enter {b.WARNING}('y', 'n' or 'q' to quit){b.ENDC}\n>> ")




