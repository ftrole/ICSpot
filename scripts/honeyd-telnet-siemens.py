#!/usr/bin/env python

# honeyd-telnet-schneider.py
#
# Copyright (C) 2006  Joel Arnold - EPFL & CERN
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

import struct, sys, signal

class TelnetSim:

  echoing = True
  logingin = True
  buffer = ""
  logintext = "\n\rSiemens Login: "
  intertext = "\n\r"
  passwtext = "\n\rPassword: "
  incortext = "\n\rLogin incorrect\n\r"

  def run(self):
    sys.stdout.write(struct.pack('BBB', 255, 251, 1))
    sys.stdout.flush()
    sys.stdout.write(self.logintext)
    sys.stdout.flush()
    try:
      def sighandler(signum, frame):
        sys.exit(0)
      signal.signal(signal.SIGALRM, sighandler)
      while True:
        signal.alarm(30)
        input = struct.unpack('B', sys.stdin.read(1))[0]
        signal.alarm(0)
        if input == 255:	# It is a command
          input = struct.unpack('B', sys.stdin.read(1))[0]
          if input == 243:	# BRK
            sys.stdout.write("0xc24068 (tTelnetInTask): telnetInTask: interrupt\n\r")
            sys.stdout.flush()
          elif input == 244:	# IP
	    sys.stdout.write("0xc24068 (tTelnetInTask): telnetInTask: interrupt\n\r")
            sys.stdout.flush()
          elif input == 246:	# AYT
            sys.stdout.write("\r\n[yes]\r\n")
            sys.stdout.flush()
          elif input == 247:	# EC
            if len(buffer) > 0:
              self.buffer = self.buffer[:len(self.buffer)-1]
              if echoing:
                sys.stdout.write(struct.pack('BBB', 8, 32, 8))
                sys.stdout.flush()
          elif input == 248:	# EL
            sys.stdout.write("\n\r")
            sys.stdout.flush()
          elif input == 251:	# WILL
            input = struct.unpack('B', sys.stdin.read(1))[0]
            if input == 1:	# ECHO
              sys.stdout.write(struct.pack('BBB', 255, 253, input))
              sys.stdout.flush()
              self.echoing = False
            else:		# Anything else
              sys.stdout.write(struct.pack('BBB', 255, 254, input))
              sys.stdout.flush()
          elif input == 252:	# WONT
            input = struct.unpack('B', sys.stdin.read(1))[0]
            if input == 1:	# ECHO
              sys.stdout.write(struct.pack('BBB', 255, 251, input))
              sys.stdout.flush()
              self.echoing = True 
            else:		# Anything else
              pass	
          elif input == 253:	# DO
            input = struct.unpack('B', sys.stdin.read(1))[0]
            if input == 1:	# ECHO
              self.echoing = True
            elif input == 3:# SGH
              sys.stdout.write(struct.pack('BBB', 255, 251, input))
              sys.stdout.flush()
            else:		# Anything else
              sys.stdout.write(struct.pack('BBB', 255, 252, input))
              sys.stdout.flush()
          elif input == 254:	# DONT
            input = struct.unpack('B', sys.stdin.read(1))[0]
            sys.stdout.write(struct.pack('BBB', 255, 252, input))
            sys.stdout.flush()
            if input == 1:
              self.echoing = True
        elif input == 127 or input == 8:# Backspace
          if len(self.buffer) > 0:
            self.buffer = self.buffer[:len(self.buffer)-1]
            if self.echoing and self.logingin:
              sys.stdout.write(struct.pack('BBB', 8, 32, 8))
              sys.stdout.flush()
        else:				# Some character, or \n etc.
          inchar = struct.unpack('c', struct.pack('B', input))[0]
          if inchar == "\r":
            nextchar = struct.unpack('B', sys.stdin.read(1))[0]
            if self.logingin :
              if len(self.buffer) > 0:
                self.logingin = False
                self.buffer = ""
                sys.stdout.write(self.intertext)
                sys.stdout.flush()
                sys.stdout.write(self.passwtext)
                sys.stdout.flush()	# Print password Prompt
              else:
                sys.stdout.write(self.intertext)
                sys.stdout.flush()
                sys.stdout.write(self.logintext)
                sys.stdout.flush()	# Print login prompt again
            else:			# Passwordingin
              self.logingin = True
              self.buffer = ""
              sys.stdout.write(self.incortext)
              sys.stdout.flush()	# Print Login incorrect
              sys.stdout.write(self.logintext)
              sys.stdout.flush()	# Print login prompt again
          else:
            self.buffer += inchar
            if self.echoing and self.logingin:
              sys.stdout.write(struct.pack('c', inchar))
              sys.stdout.flush()
    except:
      sys.exit(1)
TelnetSim().run()
