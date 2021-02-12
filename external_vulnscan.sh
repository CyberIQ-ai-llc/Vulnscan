#!/bin/bash

# Gets the user name

username=$USER

# A couple color vars 

fb='\e[1m'
cgy='\e[90m' # color dk gray
cg='\e[92m'  # color green
cb='\e[34m'  # color blue
cy='\e[33m'  # color yellow
cn='\e[0m'   # color none

# Prints VulscanX banner to screen

printf "${cb}${fb}"
figlet -w 100 VulnscanX
echo -e "${cb}\tScan External Targets\n"
echo -e "${cgy}Cyber${cb}IQ${cy}.${cb}ai, Powered by Vulscan${cn}"
 
# Invalid input handling

repeat='y'
while [[ $repeat == 'y' ]]; do
    valid='no'
    echo -e "\n${cy}You must enter a FQDN like domain.com${cn}"
    while [[ $valid == 'no' ]]; do
        echo -e "Enter the domain or IPv4 address you want to scan"
        read -p ">> " ip
        host $ip 2>&1 > /dev/null
        if [[ $? -eq 0 ]]; then
            valid='yes'
        elif [[ $ip == '192.168.'* || $ip == '10.'* ]]; then
            printf "${cy}${fb}"
            echo -e '\nThis app is not for scanning LANs'
            printf "${cn}"
        elif [[ $ip == '172.'* ]]; then
            declare -a sec_octet=( $(echo {16..31}) )
            IFS='.' read -r -a octets <<< $ip
            if [[ ${sec_octet[@]} =~ ${octets[1]} ]]; then
                printf "${cy}${fb}"
                echo -e '\nThis app is not for scanning LANs'
                printf "${cn}"
            fi
        else
            printf "${cy}${fb}"
            echo -e '\nYou have entered an invalid IP or domain.'
            printf "${cn}"
        fi
    done

    # (2) This section variable will create a directory to store the output of the scans.
    # It takes user input to name the 'directory' variable then gives the 'filename'
    # variable the same value as 'directory'.  It then appends the date/time to the value
    # of the 'directory' to make sure the directory name is unique an to know when it was 
    # created. finally it creates a directory in 'saved_nmap_scans'.

    directory=''
    echo -e "\nEnter a directory name you want to save results to"
    echo -e "${cy}[Enter]${cn} to use default or backspace and enter a new name:"
    read -e -i $ip -p ">> " directory

    filename=$directory
    directory=$directory$(date +%Y%m%d_%H%M%S)
    mkdir saved_nmap_scans/$directory

    # (3) Select ports to be scanned or use defaults.
    # NOTE: Feel free to modify the default ports.
    # I didn't bother to trap for inalid entries possibly in the future I might try
    # doing some error handling for 'ports' but that would be hard since there are
    # so many possible combinations

    ports='1-65535'
    echo -e "\n${cg}Proper formats for entering ports look like the following:"
    echo -e "22,53,80,443  NOTE: no spaces after the commas"
    echo -e "1-1024 or 1-1024,1723,3389${cn}\n"
    echo -e "\nDo you want to use the default of all ports 1-65535."
    echo -e "${cy}(Entering ANY value other than 'n' will result in the default of all ports)${cn}"
    echo -e "${cy}[Enter]${cn} to use the default or ${cy}'n'${cn} to select different ports:"
    read -p ">> " yorn

    if [[ $yorn == 'n' ]]; then
        echo -e "\nEnter the port(s) or ports range: "
        read -p ">> " ports
    fi

    # (4) This section allows the user to set the timing of the scan. Has input validation

    declare -i speed
    speed=6  # Needs to be set to a number out of the range of the below while statement.
    while [[ $speed -lt 0 || $speed -gt 5 ]]; do
        speed=4
        echo -e "\n${cy}(Slower speed may result in more accurate results)${cn}"
        echo -e "Select the speed of the scan integers 0-5:"
        read -e -i $speed -p ">> " speed
    done

    # Another banner of sorts

    printf "${cy}"
    figlet -f digital "***COMMENCING-SCAN***"
    printf "${cn}"

    # (8) This line does an indepth nmap scan doing service discovery(-sV), and runs the vulners
    # script.  It also saves the results (-oG and -oN)to chosen filename in the created directory
    # and an xml file scanfile.xml. 

    sudo nmap --script=default,vulners.nse -v -sV -T$speed -oX e_scanfile.xml -oG saved_nmap_scans/$directory/$filename.grep -oN saved_nmap_scans/$directory/$filename.txt -p$ports $ip 

    # (9) The xsltproc process creates an .html version of scanfile.xml both of these files will be overwritten
    # the next time the script is run.

    xsltproc e_scanfile.xml -o e_scanfile.html

    # (10) The next two lines create empty files of the chosen filename with the .xml and .html extensions 

    touch saved_nmap_scans/$directory/$filename.xml
    touch saved_nmap_scans/$directory/$filename.html

    # (11) The next two lines copy the contents of scanfile.xml and scanfile.html to the files created above.

    cp e_scanfile.xml  saved_nmap_scans/$directory/$filename.xml
    cp e_scanfile.html saved_nmap_scans/$directory/$filename.html

    # (12) This line takes the script out of root user by using the value of $username passed from  
    # 'vulscan.py' then opens the scanfile.html in the default browser.

    sudo -u $username xdg-open e_scanfile.html

    # (13) Prints to the screen the location of the output files.

    echo -e "\nThe following reports are available at:"
    echo -e "\n  ~/vulnscan/saved_nmap_scans/$directory/$filename.xml"
    echo -e "  ~/vulnscan/saved_nmap_scans/$directory/$filename.html"
    echo -e "  ~/vulnscan/saved_nmap_scans/$directory/$filename.txt"
    echo -e "  ~/vulnscan/saved_nmap_scans/$directory/$filename.grep"

    echo -e "\n${cg}Would you like to scan another target?${cn}"
    read -e -i $repeat -p ">> " repeat

done