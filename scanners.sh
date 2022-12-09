echo "Enter the target IP: "  
read IP

# generic scan by IP
# sudo nmap $IP

# SERVICE/VERSION DETECTION
# sudo nmap -sV $IP

# arp ping may be a problem due to the default timeout in namp (honeypot reply may be slow). This command should bypass the problem 
sudo nmap -sS -sU -Pn --disable-arp-ping -p 1-1024 -T4 -A -v $IP 

# Secific scan for s7 service 
sudo nmap --script s7-info.nse -p 102 $IP

# Sepcific scan for modubus services 
sudo nmap --script modbus-discover.nse --script-args='modbus-discover.aggressive=true' -p 502 $IP

# specific scan for snmp service and obtain the fingerprint of the PLC
# requires: sudo apt install snmp
snmpwalk -v1 -c public $IP

# check ftp connection
ftp $IP

# check telnet connection
telnet $IP
