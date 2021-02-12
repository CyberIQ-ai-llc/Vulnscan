#!/bin/bash

##### This script is a companion script to vulnscan.py and will not run on it's own
# NOTE: the 'directory' variable can be set to any value you want as a default
# or set to a blank string ''
# This is a script to do an nmap scan with vulners and render it in a browser.

# (1) 'IP' or $IP when used as a variable gets the network address from vulnscan.py
# 'username' gets the non-root username from  vulnscan.py.

IP=$1
username=$2
# A couple color vars

cg='\e[92m'  # color green
cb='\e[34m'  # color blue
cy='\e[93m'  # color yellow
cn='\e[0m'   # color none

# (2) This section variable will create a directory to store the output of the scans.
# It takes user input to name the 'directory' variable then gives the 'filename'
# variable the same value as 'directory'.  It then appends the date/time to the value
# of the 'directory' to make sure the directory name is unique an to know when it was 
# created. finally it creates a directory in 'saved_nmap_scans'.

directory='ATT_home_'
echo -e "\nEnter a directory name you want to save results to"
echo -e "$cy[Enter]$cn to use default or backspace and enter a new name:"
read -e -i $directory -p ">> " directory

filename=$directory
directory=$directory$(date +%Y%m%d_%H%M%S)
mkdir saved_nmap_scans/$directory

# (3) Select ports to be scanned or use defaults.
# NOTE: Feel free to modify the default ports.
# I didn't bother to trap for inalid entries possibly in the future I might try
# doing some error handling for 'ports' but that would be hard since there are 
# so many possible combinations

ports='1-65535'
echo -e "$cg\nProper formats for entering ports look like the following:"
echo -e "22,53,80,443  NOTE: no spaces after the commas"
echo -e "1-1024 or 1-1024,1723,3389$cn\n"
echo -e "Do you want to use the default of all ports 1-65535."
echo -e "$cy(Entering ANY value other than 'n' will result in the default of all ports)$cn"
echo -e "$cy[Enter]$cn to use the default or $cy'n'$cn to select different ports:"
read -p ">> " yorn

if [[ $yorn == 'n' ]]; then
    echo -e "\nEnter the port(s) or ports range: "
    read -p ">> " ports
fi

# (4) This section allows the user to set the Timing of the scan.

speed=6  # Needs to be set to a number out of the range of the below while statement.
while [[ $speed -lt 0 || $speed -gt 5 ]]; do
    speed=4
    echo -e "\n$cy(Slower speed may result in more accurate results)$cn"
    echo -e "Select the speed of the scan integers 0-5:"
    read -e -i $speed -p ">> " speed
done

# (5) This is a host discovery scan.  The nmap_grep.txt file is overwritten each time the script is run

sudo nmap -v -sn -PU T4 -oG nmap_grep.txt $IP   # I switched out -PU fo this --disable-arp-ping

# (6) This line filters out the 'Up' 'Hosts' and checks for unique values then 
# saves them to 'up_hosts.txt' in the created 'directory'.

cat nmap_grep.txt | grep 'Host' | grep 'Up' | uniq > saved_nmap_scans/$directory/up_hosts.txt

# (7) This line filters out the IPs in nmap_grep.txt and checks for unique values then 
# puts them in the input_list.txt file
# The input_list.txt file will be overwritten on each run of the script.

cat nmap_grep.txt | grep 'Host' | grep 'Up' | awk '{ print $2 }' | uniq > input_list.txt

# (8) This line does an indepth nmap scan doing service discovery(-sV), and runs the vulners
# script.  It also saves the results (-oG and -oN)to chosen filename in the created directory
# and an xml file scanfile.xml. 

nmap --script=default,vulners.nse -v -Pn -sV -T$speed -iL input_list.txt -oX scanfile.xml -oG saved_nmap_scans/$directory/$filename.grep -oN saved_nmap_scans/$directory/$filename.txt -p$ports $IP  ## $port ,vulscan --script-args vulscandb=exploitdb.csv 

# (9) The xsltproc process creates an .html version of scanfile.xml both of these files will be overwritten
# the next time the script is run.

xsltproc scanfile.xml -o scanfile.html

# (10) The next two lines create empty files of the chosen filename with the .xml and .html extensions 

touch saved_nmap_scans/$directory/$filename.xml
touch saved_nmap_scans/$directory/$filename.html

# (11) The next two lines copy the contents of scanfile.xml and scanfile.html to the files created above.

cp scanfile.xml  saved_nmap_scans/$directory/$filename.xml
cp scanfile.html saved_nmap_scans/$directory/$filename.html

# (12) This line takes the script out of root user by using the value of $username passed from  
# 'vulscan.py' then opens the scanfile.html in the default browser.

sudo -u $username xdg-open scanfile.html

# (13) Prints to the screen the location of the output files.

echo -e "\nThe following reports are available at:"
echo -e "\n  ~/vulnscan/saved_nmap_scans/$directory/$filename.xml"
echo -e "  ~/vulnscan/saved_nmap_scans/$directory/$filename.html"
echo -e "  ~/vulnscan/saved_nmap_scans/$directory/$filename.txt"
echo -e "  ~/vulnscan/saved_nmap_scans/$directory/$filename.grep"
echo -e "  ~/vulnscan/saved_nmap_scans/$directory/up_hosts.txt\n"



