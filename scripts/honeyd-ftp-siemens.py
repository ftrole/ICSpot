#!/usr/bin/env python 

# honeyd-ftp-siemens.py
#
# Copyright (C) 2006  Joel Arnold - EPFL & CERN
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

import re, sys, os, signal

inittext = "220 CP 343-1 IT FTP-Server V1.36 ready for new user\r\n"
helptext = "214-The following commands are recognized (* =>'s unimplemented).\r\n     USER\tPWD\tLIST\tRETR\tMODE\tREST\tAPPE*\n     PASS\tMKD\tNLST\tSTOR\tSTRU\tABOR\tREIN*\n     QUIT\tRMD\tRNFR\tPORT\tHELP\tNOOP\tSITE*\n     CWD\tXMKD\tRNTO\tPASV\tSTAT\tACCT*\tSMNT*\n     CDUP\tXRMD\tDELE\tTYPE\tSYST\tALLO*\tSTOU*\n214 End of help.\r\n"
passtext = "530 Not logged in.\r\n"
quittext = "221 Closing control connection; Thank you for using our FTP server.\r\n"
systtext = "215 CP x43-1 IT Type: L8\r\n"
usertext = "530 Not logged in.\r\n"
elsetext = "530 Not logged in.\r\n"
commtext = "200 Command okay.\r\n"
stattext = ""
touttext = "221 Timeout. Closing control connection.\r\n"

class FTPSim:

  def run(self):
    global stattext
    #remote_host = os.environ['HONEYD_IP_SRC']
    remote_host = '192.168.1.200'
    stattext = "211-CP 343-1 IT FTP-Server V1.36\r\n     Connected to " + remote_host + "\n     Not logged in\n    TYPE: ASCII, FORM: Nonprint; STRUcture: File; transfer MODE: Stream\n211 End of status\r\n"
    sys.stdout.write(inittext)
    sys.stdout.flush()
    while True:
      try:
        self.parseInput()
      except:
        sys.exit(0)

  def parseInput(self):
    close = False
    def sighandler(signum, frame):
      sys.stdout.write(touttext)
      sys.stdout.flush()
      sys.exit(0)
    signal.signal(signal.SIGALRM, sighandler)
    signal.alarm(100)
    requestline = sys.stdin.readline()
    signal.alarm(0)
    if (requestline == "\n" or requestline == "\r\n"):
      sys.stdout.write(elsetext)
      sys.stdout.flush()
      return
    if (requestline == ""):
      sys.exit(0)
    requestparser = re.compile('(\S{4})(.*)')
    try:
      (method, args) = requestparser.match(requestline.strip()).groups()
      method = method.upper()
      if method.startswith('HELP'):
        sys.stdout.write(helptext)
        sys.stdout.flush()
      elif method.startswith('PASS'):
        sys.stdout.write(passtext)
        sys.stdout.flush()
      elif method.startswith('QUIT'):
        sys.stdout.write(quittext)
        sys.stdout.flush()
        close = True
      elif method.startswith('SYST'):
        sys.stdout.write(systtext)
        sys.stdout.flush()
      elif method.startswith('USER'):
        sys.stdout.write(usertext)
        sys.stdout.flush()
      elif method.startswith('STAT'):
        sys.stdout.write(stattext)
        sys.stdout.flush()
      elif method.startswith('ABOR'):
        sys.stdout.write(commtext)
        sys.stdout.flush()
      elif method.startswith('NOOP'):
        sys.stdout.write(commtext)
        sys.stdout.flush()
      else:
        sys.stdout.write(elsetext)
        sys.stdout.flush()
    except:
      sys.stdout.write(elsetext)
      sys.stdout.flush()

    if (close == True):
      sys.exit(0)

FTPSim().run()
