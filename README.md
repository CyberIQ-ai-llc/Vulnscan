# Vulnscan

CyberIQ Vulnscan uses Nmap and Vulners to scan an external target or internal network for vulnerabilities. It makes the process a little simpler by prompting you for the values that Nmap uses in its comman line arguments. It will guide you through selecting the targets, ports and scan speed.

It is a combination of Python and Bash scripts that automatically determine your IP address, CIDR, broadcast address, gateway, and network address for internal scans.

External_vulnscan will scan an external IP address or web application.

When finished, Vulnscan will display the output of the Nmap/Vulners scan in a web browser.

Give execute rights to the scripts: 
sudo chmod +x external_vulnscan.sh vulnscan.sh

Goto your nmap scripts: 
cd /usr/share/nmap/scripts/

Clone the Vulners git:
sudo git clone https://github.com/vulnersCom/nmap-vu...​

Install netifaces module command: 
sudo pip install netifaces
