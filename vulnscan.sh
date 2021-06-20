#!/bin/bash

# In each of the case statements you have the option of setting a default choice or selecting a choice every
# time. You will probably find that you use the same choices most of the time. To switch to having
# a default, for each case statement that you want to have a default, uncomment the two lines following the 
# while statement, set the number value for the choice variable (no spaces) and comment out the following read
# prompt. This was initially for testing but found them useful for general use or for repeating a monthly scan.
# There were some intermitten errors with using Edge Chromium browser as the default browser, If you are 
# experencing issues at the end of the script uncomment:
#"#sudo -u $username firefox saved_nmap_scans/$directory/$filename.html&"
# and comment out: 
#"sudo -u $username xdg-open saved_nmap_scans/$directory/$filename.html&"
# Running in a terminal in VS Code has the added benefit of allowing to quickly view the files in the code editor.


ip=$1
username=$2
declare -i oops=0

cg='\e[92m'
cb='\e[34m'
cy='\e[93m'
cn='\e[0m'

directory='nmap_'    # Edit to change your default

clear

echo -e "\n${cy}Your current scan: ${cg}sudo nmap -Pn -sS $ip${cn}"
echo -e "\nEnter a directory name you want to save results to"
echo -e "$cy[Enter]$cn to use default or backspace and enter a new name:"
read -e -i $directory -p ">> " directory

filename=$directory
directory=$directory$(date +%m_%d_%Y_%H:%M:%S)
mkdir saved_nmap_scans/$directory

clear

echo -e "\n${cy}Your current scan:${cn} sudo nmap -Pn -sS ${cg}-oA saved_nmap_scans/$directory/$filename${cn} $ip"

echo -e "\nSet ports to be scanned"
echo -e "\t1) Top 1000........(Default if no ports given)" 
echo -e "\t2) Top 100.........(-F)" 
echo -e "\t3) All 65535 ports.(-p-)"
echo -e "\t4) Select ports to scan"

while [[ $oops == 0 ]]; do
    #choice=3                                 
    #read -e -i $choice -p ">>> " choice
    read -p ">>> " choice
    case $choice in
        1) ports=''
           oops=1
           ;;
        2) ports='-F'
           oops=1
           ;;
        3) ports="-p-"
           oops=1
           ;;
        4) echo -e "Enter the port/s you wish to scan seperated by commas no spaces or a range like 1-1024"
           read -e -p '>>> ' ports
           ports='-p'$ports
           oops=1
           ;;
        *) echo -e "Invalid input please enter 1-4"
           ;;
    esac      
done

clear

echo -e "\n${cy}Your current scan:${cn} sudo nmap ${cg}$ports${cn} -Pn -sS -oA saved_nmap_scans/$directory/$filename $ip"

oops=0
echo -e "\nSet scan timing"
echo -e "\t0) Paranoid...(-T0)"
echo -e "\t1) Sneaky.....(-T1)"
echo -e "\t2) Polite.....(-T2)"
echo -e "\t3) Normal.....(-T3)"
echo -e "\t4) Agressive..(-T4)"
echo -e "\t5) Insane.....(-T5)" 

while [[ $oops == 0 ]]; do
    #choice=4                                 
    #read -e -i $choice -p ">>> " choice
    read -p ">>> " choice
    case $choice in
        0) speed='-T0'
           oops=1
           ;;
        1) speed='-T1'
           oops=1
           ;;
        2) speed='-T2'
           oops=1
           ;;
        3) speed='-T3'
           oops=1
           ;;
        4) speed='-T4'
           oops=1
           ;;
        5) speed='-T5'
           oops=1
           ;;
        *) echo -e "Invalid input please enter 0-5"
           ;;
    esac      
done

clear

echo -e "\n${cy}Your current scan:${cn} sudo nmap $ports ${cg}$speed${cn} -Pn -sS -oA saved_nmap_scans/$directory/$filename $ip"

oops=0
echo -e "\nEnter verbosity level"
echo -e "\t0) Silent (-q)"
echo -e "\t1) -v"
echo -e "\t2) -vv"
echo -e "\t3) -vvv"
echo -e "\t4) -vvvv"
echo -e "\t5) Default verbosity"

while [[ $oops == 0 ]]; do
    #choice=3                                 
    #read -e -i $choice -p ">>> " choice
    read -p ">>> " choice
    case $choice in
        0) verbosity='-q'
           oops=1
           ;;
        1) verbosity='-v'
           oops=1
           ;;
        2) verbosity='-vv'
           oops=1
           ;;
        3) verbosity='-vvv'
           oops=1
           ;;
        4) verbosity='-vvvv'
           oops=1
           ;;
        5) verbosity=''
           oops=1
           ;;
        *) echo -e "Invalid input please enter 0-5"
           ;;
    esac      
done

clear

echo -e "\n${cy}Your current scan:${cn} sudo nmap $ports $speed ${cg}$verbosity${cn} -Pn -sS -oA saved_nmap_scans/$directory/$filename $ip"

echo -e "\nSet service and OS discovery"
echo -e "\t0) No service or OS discovery"
echo -e "\t1) Service discovery only........(-sV)"
echo -e "\t2) OS discovery only.............(-O)"
echo -e "\t3) Both service and OS discovery.(-sV -0)"

oops=0
while [[ $oops == 0 ]]; do
    #choice=4                                 
    #read -e -i $choice -p ">>> " choice
    read -p ">>> " choice
    case $choice in
        0) disc=''
           oops=1
           ;;
        1) disc='-sV'
           oops=1
           ;;
        2) disc='-O'
           oops=1
           ;;
        3) disc='-sV -O'
           oops=1
           ;;
        *) echo -e "Invalid input please enter 0-3"
           ;;
    esac      
done

clear

echo -e "\n${cy}Your current scan:${cn} sudo nmap $ports $speed $verbosity ${cg}$disc${cn} -Pn -sS -oA saved_nmap_scans/$directory/$filename $ip"

echo -e "\nSet nmap scripting engines to run"
echo -e "\t0) None"
echo -e "\t1) default only....(--script=default or -sC)"
echo -e "\t2) vuln only.......(--script=vuln)"
echo -e "\t3) vulners only....(--script=vulners.nse)"
echo -e "\t4) Run all of them.(--script=default,vuln,vulners.nse)"

oops=0
while [[ $oops == 0 ]]; do
    #choice=4                                 
    #read -e -i $choice -p ">>> " choice
    read -p ">>> " choice
    case $choice in
        0) script=''
           oops=1
           ;;
        1) script='--script=default'
           oops=1
           ;;
        2) script='--script=vuln'
           oops=1
           ;;
        3) script='--script=vulners.nse'
           oops=1
           ;;
        4) script='--script=default,vuln,vulners.nse'
           oops=1
           ;;
        *) echo -e "Invalid input please enter 0-4"
           ;;
    esac      
done

clear

scan="$script $ports $speed $verbosity $disc -Pn -sS -iL saved_nmap_scans/$directory/input_list.txt -oA saved_nmap_scans/$directory/$filename $ip"
# echo -e "$scan" >> test.txt
echo -e "\nThis script will generate an input list during host discovery which will be added to your scan\n"
echo -e "\n${cy}Your current scan:${cn} sudo nmap ${cg}$script${cn} $ports $speed $verbosity $disc -Pn ${cg}-iL saved_nmap_scans/$directory/input_list.txt${cn} -oA saved_nmap_scans/$directory/$filename $ip"
echo -e "\n${cb}You can press [?] during scan to view Interactive keyboard commands:${cn}\n"
read -e -p "Press [Enter] to continue" pause

sudo nmap -sn -PA -T4 -oG saved_nmap_scans/$directory/$filename.gnmap $ip
cat saved_nmap_scans/$directory/$filename.gnmap | grep 'Host' | grep 'Up' | uniq > saved_nmap_scans/$directory/up_hosts.txt
cat saved_nmap_scans/$directory/up_hosts.txt | grep 'Host' | awk '{ print $2 }' | uniq > saved_nmap_scans/$directory/input_list.txt
sudo rm -r saved_nmap_scans/$directory/$filename.gnmap

sudo nmap $scan

xsltproc saved_nmap_scans/$directory/$filename.xml -o saved_nmap_scans/$directory/$filename.html

sudo -u $username xdg-open saved_nmap_scans/$directory/$filename.html&
#sudo -u $username firefox saved_nmap_scans/$directory/$filename.html&

echo -e "\nThe following reports are available at:"
echo -e "\n  ${cg}~/Vulnscan/saved_nmap_scans/$directory/$filename.nmap"
echo -e "  ~/Vulnscan/saved_nmap_scans/$directory/$filename.xml"
echo -e "  ~/Vulnscan/saved_nmap_scans/$directory/$filename.html"
echo -e "  ~/Vulnscan/saved_nmap_scans/$directory/$filename.gnmap"
echo -e "  ~/Vulnscan/saved_nmap_scans/$directory/up_hosts.txt"
echo -e "  ~/Vulnscan/saved_nmap_scans/$directory/input_list.txt${cn}"
