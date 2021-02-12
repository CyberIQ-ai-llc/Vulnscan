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
    banner = pyfiglet.figlet_format("Vulnscan")
    print(f"\n{b.OKBLUE}{b.BOLD}{banner}{b.ENDC}")
except ModuleNotFoundError:
    pass

print(f"\t{b.OKBLUE}{b.BOLD}Get Net Info & Scan Your Network{b.ENDC}")
print(f"\n{b.BOLD}{b.CGREY}Cyber{b.OKBLUE}IQ{b.WARNING}.{b.OKBLUE}ai, {b.ENDC}Powered by Vulners")

""" (10) This section prints out the results """

print(f"\n{b.WARNING}You can type {b.OKBLUE}Ctrl^C{b.WARNING} at any time to quit.{b.ENDC}")
print(f"\n{b.OKGREEN}The IP address of your computer is: {b.ENDC}{b.BOLD}{host}{b.ENDC}")
print(f"{b.OKGREEN}The network netmask is: {b.ENDC}{b.BOLD}{netmask}{b.ENDC}")
print(f"{b.OKGREEN}The broadcast address is: {b.ENDC}{b.BOLD}{broadcast}{b.ENDC}")
print(f"{b.OKGREEN}The gateway address is: {b.ENDC}{b.BOLD}{gateway}{b.ENDC}")
print(f"{b.OKGREEN}The network CIDR range is: {b.ENDC}{b.BOLD}{CIDR}{b.ENDC}")

""" (11)This line asks the user if they want to use the network address generated from
    the above script asking for a 'y', 'n' or 'q' and storing the value in the 'choice1' variable"""

choice1 = input(f"{b.OKGREEN}The network address is: {b.ENDC}{b.BOLD}{net_addr}{b.ENDC}\n\nDo you want to scan the entire {b.BOLD}{net_addr}{b.ENDC} network? {b.WARNING}('y', 'n' or 'q' to quit){b.ENDC}\n(default=y)>> ") or "y"

flag = 0
CIDR_flag = 0
verify_IP = ''

""" (12) This section takes the user input from 'choice1'. *(option 1) If 'choice1 == 'y'' it takes the default 
    values from the previous code and run 'vulscan.sh'. *(option 2) If 'choice1 == 'n'' the user is prompted 
    to enter an IPv4 address.  (12*) It then calls the 'n.check_IP() function passing the entered IP
    and checks it for proper IPv4 format (NOTE: it does not mean that it is an actual IPv4 address it just 
    means it fits within the XXX.XXX.XXX.XXX format where each group of X's can be 1-3 in length and be within
    the range of (0-255).  If IP is verified it breaks out of the loop. *(option3)) If 'choice1 == 'q'' the program is exited.  
    *(invalid input) none of the 'if/elif' statements are met, the user is reprompted for 'choice1' value and is 
    returned to the beginning of the loop."""

while True:
    # (option 1)
    if choice1.lower() == 'y':
        subprocess.call(shlex.split(f"sudo ./vulnscan.sh {net_addr} {username}"))
        exit()  # I added this exit because for some reason the .sh script was looping back to the beginning, this seemed to solve the problem
        break
    # (option 2)      
    elif choice1.lower() == 'n':
        IP_addr = input(f"\n{b.WARNING}(If you wish to enter a CIDR range you will be prompted later).{b.ENDC}\nEnter the IPv4 address to be scanned\n(default={net_addr_no_CIDR})>> ") or net_addr_no_CIDR
        verify_IP, flag = n.check_IP(IP_addr)   #
        if flag == 0:
            print(f"\n\t{b.FAIL}{verify_IP}{b.ENDC}")
        if flag == 1:
            break
    # (option 3)      
    elif choice1.lower() == 'q':
        exit()
    # (invalid input)
    else:
        choice1 = input(f"\n\t{b.FAIL}(Invalid input)\n\n{b.ENDC}Please enter {b.WARNING}('y', 'n' or 'q' to quit){b.ENDC}\n>> ")

""" (13) This section first prompts the user if they want to enter a CIDR range for the scan 
    prompting with a value of 'y' or 'n'.  *(option1) If 'choice2 == y' the user is prompted to enter a 
    CIDR range 'CIDR_rng' and is given some instruction on what a CIDR should look like.  The users input is then
    checked for proper format (NOTE: once again this does not verify that it is the appropriate range 
    just that it falls within the allowed values for a CIDR).  If it is a valid CIDR the loop ends if not 
    valid the user is reprompted to enter a new value.  *(option2) If 'choice2 == n' the loop ends. 
    *(option3) Neither of the two options are met an the user is prompted to reenter the value for 'choice2' 
    and returned to the begining of the loop. """

choice2 = input(f"\nWould you like to enter a CIDR range? {b.WARNING}('y' or 'n'){b.ENDC}\n(default=y)>> ") or 'y'
CIDR_flag = 0
while True:
    if choice2.lower() == 'y':
        print(f"\n{b.OKGREEN}REMINDER: {b.ENDC}Your current network CIDR range is: {b.BOLD}{CIDR}{b.ENDC}")
        CIDR_rng = input(f"Please enter your CIDR range {b.WARNING}(0-32, most common 24){b.ENDC}.\n(default={CIDR})>> ") or CIDR
        verify_CIDR, CIDR_flag = n.check_CIDR(CIDR_rng)
        if CIDR_flag == 0:
            print(f"\n\t{b.FAIL}{verify_CIDR}{b.ENDC}")
        if CIDR_flag == 1:
            break
    elif choice2.lower() == 'n':
        break
    else:
        choice2 = input(f"\n\t{b.FAIL}(Invalid input){b.ENDC}\n\nPlease enter {b.WARNING}('y', 'n'){b.ENDC}\n>> ")

""" (14) NOTE: I am no longer using this section. I put this section in because the host discovery for some reason was 
    missing the gateway address, but I solved this by changing the host scan. I left it in incase I found a future use for it.
    This section splits the IP adderess into individual octets as a dictionay as a key/value pair like {octet1: 192, octet2: 168, octet3: 0, octet4: 0} 
    to be used in 'vulnscan.sh'. """

octets_dict = n.split_net_addr(verify_IP)
octet1, octet2, octet3, octet4 = '', '', '', ''
locals().update(octets_dict)

""" (15) This section checks for if the user chose to user a CIDR range if 'y' appends a '/' and 'verify_CIDR
    to 'verify_IP' and stores it in 'net_addr'. If user chose not to enter a CIDR the value of 
    verify_IP is stored in 'net_addr'. """

if CIDR_flag == 1:
    net_addr = verify_IP + '/' + verify_CIDR
else:
    net_addr = verify_IP

""" (16) This line calls the 'vulnscan.sh' and passes the values of an IP address or network and the username. """

subprocess.call(shlex.split(f"sudo ./vulnscan.sh {net_addr} {username}"))

