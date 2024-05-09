# run this script in order to obtain a honeyd log file cleaned 
# from the packet storm on port 8000 caused by the HMI periodical refresh
# you must provide honeyd.log as argument and will obtain honeyd_clean.log as result


#!/usr/bin/env python3
import sys
import os

analyzed=0
prev_line=""

logFile = sys.argv[1]
with open(logFile) as f:
    logList = f.readlines()

f= open("honeyd_clean.log","w+")

for line in logList:
    # parse every line
    analyzed = analyzed + 1
    if not "8000" in line or not "E" in line or not "8000" in prev_line or not "E" in prev_line:
    # write line in the clean log file
      f.write(line)
    prev_line=line

f.close()
    	        
os.system('clear')
print("Analyzed " + str(analyzed) + " log liness")
