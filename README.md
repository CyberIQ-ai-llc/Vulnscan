# Vulnscan

We have made some changes to Vulnscan. It no longer has the option of a single device scan and is strictly a whole network scanner. This makes it a good tool for doing periodic network scans. It now also has more options for the intensity of the scan and displays the current nmap scan as you go through the menus. If you wish to have default choices for your scan, you can do a little editing to the vulnscan.sh script.  For each of the case statements (there are 5 instances) where you see the while statement change this:
                                                                                                                                    
    #choice=3                               # Change these lines 
    #read -e -i $choice -p ">>> " choice    # 
    read -p ">>> " choice                   # 
    
To: 

    choice=3                                # To this and edit the value of the choice variable
    read -e -i $choice -p ">>> " choice     # to the menu value that you want
    #read -p ">>> " choice                  #
    
The default values that are currently set are for a very intensive vulnerability scan

There were some intermitten errors with using Edge Chromium browser as the default browser, If you are experencing issues at the end of the script

Uncomment:  "#sudo -u $username firefox saved_nmap_scans/$directory/$filename.html&"  You can also substitute "firefox" for another browser

Comment out:  "sudo -u $username xdg-open saved_nmap_scans/$directory/$filename.html&"   

It is a combination of Python and Bash scripts that automatically determine your IP address, CIDR, broadcast address, gateway, and network address for internal scans.

External_vulnscan will scan an external IP address or web application.

When finished, Vulnscan will display the output of the Nmap/Vulners scan in a web browser

I plan to make a video of the latest version the video below is of the old vervion                                                                                
https://www.youtube.com/watch?v=bz-YNAqkEdw&list=PL-wIeEEXVEaNRC2XkOeo8crDXoiToTA9E&index=1

Give execute rights to the scripts: 
sudo chmod +x external_vulnscan.sh vulnscan.sh

Goto your nmap scripts: 
cd /usr/share/nmap/scripts/

Clone the Vulners git:
sudo git clone https://github.com/vulnersCom/nmap-vulners

Install netifaces module command: 
sudo pip install netifaces

To run vulnscan:                                                                                                                                                   
cd path/to/vulnscan                                                                                                                                               
python3 vulnscan.py


