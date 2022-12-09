# generic scan by IP
nmap IP

# SERVICE/VERSION DETECTION
nmap -sV IP

# Generic scan but deeper
nmap -sS -sU -p 1-1024 -T4 -A -v IP

# Secific scan for s7 service 
#nmap --script s7-info.nse -p 102 IP

# Sepcific scan for modubus services 
nmap --script modbus-discover.nse --script-args='modbus-discover.aggressive=true' -p 502 IP

# specific scan for snmp service and obtain the fingerprint of the PLC
# requires: sudo apt install snmp
snmpwalk -v1 -c public IP
