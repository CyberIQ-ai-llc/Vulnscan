#!/bin/Python3

""" This Module is necessary for 'vulnscan.py' to run and must be in the same directory 
    it could also be used to do some more manual network calculating functions"""

from bcolors import bcolors as b                # Adds some color

 
""" (3) This function get_split_binary_function() converts the netmask and 
    broadcast addr to binary and splits them into a list of binary digits """

def get_split_binary_list(IPv4):
    binary = ''                                  # A string containing the binary of an octet.
    binary_list = []                             # A list to temporarily store the binary octets of the broadcasr address.
    split_binary_list =[]                        # A list of the individual digits of the binary broadcast address.
    octets_list = IPv4.split('.')

    for i in octets_list:  
        binary = format(int(i), '08b')           # Use format '08b' to add leading '0' to form '8' digits of binary 'b'.
        binary_list.append(binary)               # Appends each octet 'broadcast_octets to the broadcast_binary_list'.
    join_binary = ''.join(binary_list)           # joins the four octets in broadcast_binary_list and puts join_broadcast_binary.

    for char in join_binary:
        split_binary_list.append(char)
    join_binary = ''                             # splits join_broadcast_binary and appends to split_broadcast_binary_list.
    
    return split_binary_list                     # A string o temporarily store the joined values of 'broadcast_binary_list.
    

""" (5) This function anding() compares the two binary lists ANDING to get the 
    network binary IPv4 address"""

def anding(broadcast_split_binary_list, netmask_split_binary_list):
    broadcast_bit = ''              # A variable to temporarily store the value of the first digit of 'split_broadcast_binary_list'.
    netmask_bit = ''                # A variable to temporarily store the value of the first digit of 'split_netmask_binary_list'.
    bit = ''                        # A variable to temporarily store the value of the current digit to be added to 'network_id_list'.
    network_id_list = []            # A list to store the individual binary digit of the netmask

    while netmask_split_binary_list:                      # Loops through the spl_b_list until empty
        broadcast_bit = broadcast_split_binary_list.pop(0)  # Pops the first items from split_broadcast/netmask_binary_lists
        netmask_bit = netmask_split_binary_list.pop(0)
              
        if broadcast_bit == '1' and netmask_bit == '1':     # Compares the entries if both equal 1
            bit = '1'                       
            network_id_list.append(bit)                     # a '1' is appended to the network_id_list
        else:
            bit = '0'
            network_id_list.append(bit)                     # if not a match a '0' is appended
    
    return network_id_list


""" (7) This function cidr_calculator() takes the netmask and detemines the CIDR range """

def cidr_calculator(netmask):
    switcher = {'255':0,'254':1,'252':2,'248':3,'240':4,'224':5,'192':6,'128':7,'0':8} # A python alternative to a case statement.
    cidr_calc = int(0)                       # Set the initial value of 'cidr_calc' to int(0).             
    last_cidr_calc = 0                       # Set the initial value of 'last_cidr_calc' to 0.
    CIDR = 32 
    netmask_octets_list = netmask.split('.') # Set the initial value of 'CIDR' to 32.
    for nm_oct in netmask_octets_list:
        cidr_calc = switcher.get(nm_oct,)    # Gets the corresponding value from the switcher dictionary.
        cidr_calc += last_cidr_calc          # Adds the value of the 'last_cidr_calc' to the current 'cidr_calc'.
        last_cidr_calc = cidr_calc           # Sets the value of 'last_cidr_calc' to the value of the current 'cidr_calc'.
    CIDR = CIDR - int(cidr_calc)             # Subtracts the 'cidr_calc' value from he initial value.
    return CIDR


""" (9) This function converts the list of binary digits, 'network_id_list' 
    into standard IPv4 and appends the CIDR range """

def get_net_addr(network_id_list, CIDR):
    octet = 0               # Temporarily stores each octet.
    i = 1                   # An index for creating the keys in the octets dictionary.               
    bit_value = 128         # The start value for calculating an octet.
    oct_end = 7             # Is the value that triggers the end of the last bit of an octet.
    bit_ctr = 0             # A counter value to compare to 'oct_end'
    octets = {}             # A dictionary to hold the values of individual octets.
    net_addr = ''
    net_addr_list = []
    # Takes each bit in the 'network_id_list' in groups of eight and calculates the standard IPv4 address.

    for bit in network_id_list:             # Loops through each 'bit' in 'network_id_list'.
        if bit == '1':                      # Compares the current 'bit' to the value '1'.
            octet += bit_value              # Increment the value of 'bit_value'.                                             
            bit_value = bit_value / 2       # Divides 'bit_value' by 2 to get the value of the next bit in the octet.
            bit_ctr += 1                    # increments the value of 'bit_ctr' by 1 for the end of octet.
        else:                               # Else performs the last two functions above without incrementing the octet.                                       
            bit_value = bit_value / 2
            bit_ctr += 1
        if bit_ctr <= oct_end:                  # Compares 'bit_ctr' to 'oct_end' for when to end the octet and passes back to the for                        
            pass                                # loop as long as the condition is true
        else:                                   # When if is false
            bit_value = 128                     # Reset the 'bit_value' to the first bit on '1' value
            oct_end += 8                        # Increments the 'oct_end' value by 8
            octet = int(octet)                  # Because division is being formed 'octet' is in float value (192.0) this changes to integer (192) 
            net_addr_list.append(str(octet))    # Appends the octet to net_addr_listthe join statement after the for loop needs the octets to be in 'str'
            octets['octet'+str(i)] = octet      # Creates a new key/value pair for the octets dict ie: {octet1: 192, octet2: 168,}
            i += 1                              # Increments the 'i' value by '1' for the next dict key
            octet = 0
    net_addr_no_CIDR = '.'.join(net_addr_list)  # Resets the octet value to 0 for the next octet.
    net_addr = '.'.join(net_addr_list) + '/' + str(CIDR)

    gateway_list = net_addr_list
    last_gateway_octet = gateway_list.pop(3)
    last_gateway_octet = int(last_gateway_octet) + 1
    last_gateway_octet = str(last_gateway_octet)
    gateway_list.append(last_gateway_octet)
    gateway = '.'.join(net_addr_list)
    
    return net_addr, octets, net_addr_no_CIDR, gateway


""" (12*) This function takes the user input of an IPv4 address and checks it for proper format"""

def  check_IP(IP_addr):                         # Initializing necessary variables
    flag = 0
    flag = int(flag)
    message = "(Invalid IPv4 address)"
    IP_addr_octets = []

    IP_addr_octets = IP_addr.split('.')         # Splits the IP on the .'s
    
    if len(IP_addr_octets) != 4:                # Checks the length of the list 'IP_addr_octets' if lenghth is 
        return message, flag                    # not equal to 4 the fail message and a flag of 0 is returned (ends function)

    verified_octets = []                            
    for octet in IP_addr_octets:                # If above is true
        try:                                    # Checks fo non integer characters 
            octet = int(octet)
        except ValueError:                      # If an exception is raised
            return message, flag                # The fail message and flag 0 is returned
        if octet in range(0, 256):              # Checks for proper octet values
            octet = str(octet)                  # Converts to string
            verified_octets.append(octet)       # Appends the octet to the 'verified_octets' list
        else:                                   # Integers out of range
            return message, flag                # The fail message and flag 0 is returned
    message = '.'.join(verified_octets)         # The 'verified_octets' is joined with .'s and stored in message
    flag = 1                                    # flag set to 1                    
    return message, flag                        # message and flag are returned


""" (13*) This function verifies if the user input for a CIDR range is valid number it does
    not check if it is appropriate for the network being scanned user is given a reminder
    in the main code of the correct CIDR for current network."""

def check_CIDR(CIDR_input):
    CIDR_flag = 0
    CIDR_flag = int(CIDR_flag)
    message = "(Invalid CIDR range)"
    
    try:
        CIDR_input = int(CIDR_input)            # Checks for non integer characters
    except ValueError:
        return message, CIDR_flag               # Returns error message and flag 0

    if CIDR_input in range(0,33):               # Check if CIDR is in proper range
        CIDR_input = str(CIDR_input)            # Converts to a string
        CIDR_flag = 1                           # Sets CIDR_flag to 1
        message = CIDR_input                    # Sets 'message' to the value of 'CIDR_input' 
        return message, CIDR_flag               # Returns 'message' and 'CIDR_flag'
    else:                                       # For out of range
        return message, CIDR_flag               # Returns fail message and flag 0

""" (14*) NOTE: I am no longer using this section. I put this section in because the host discovery for some reason was 
    missing the gateway address, but I solved this by changing the host scan. I left it in incase I found a future use for it.
    This function takes a IP address and creates a dictionary consisting of keys as octet# 
    and the value of the octet number"""

def split_net_addr(net_addr):
    octets = {}
    i = 1
    net_addr_list = []
    net_addr_list = net_addr.split('.')         # Splits the IP on the .'s and stores in 'net_addr_lits'
    for octet in net_addr_list:
        octets['octet'+str(i)] = octet          # Creates a new key/value pair for the octets dict ie: {octet1: 192, octet2: 168,}
        i += 1                                  # Increments the 'i' value by '1' for the next dict key
        octet = 0                               # Resets the octet value to 0 for the next octet.
    return octets                               # Returns the octets dictionary 

