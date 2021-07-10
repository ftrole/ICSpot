#!/usr/bin/env python 

# honeyd-http-siemens.py
#
# Copyright (C) 2006  Joel Arnold - EPFL & CERN
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

import re, sys, time, os

webroot = "/home/ubuntu/Desktop/CSH_20060623/cernscadahoneynet/files/scripts/web-siemens"
#webroot = "/home/ubuntu/Desktop/CSH_20060623/cernscadahoneynet/files/scripts/web-siemens"

class HTTPSim:
  def run(self):
    while True:
      try:
        self.parseInput()
      except:
        sys.exit(0)

  def parseInput(self):
  	
    requestline = sys.stdin.readline()
  	
    blanklines = [ "\r\n", "\n", "" ]
  	
    try:
      method, path = re.findall('(\S+)\s+(\S+)', requestline)[0]
    	
    except:
      self.badrequest()

    else:
      requestline = sys.stdin.readline()
      while (requestline not in blanklines):
        requestline = sys.stdin.readline()
    	
      if (path == "/__Send_Test_Mail"):
        self.testmail()

      temppath = re.sub('/\.{1,2}/', '//', path)
      if (not os.path.exists(webroot + temppath)):
        self.notfound(path)
    	
      if (method == "POST"):
        self.notallowed(path)
    	
      if (method != "GET" and method != "HEAD"):
        self.unimplemented(path)
    	
      if ((path != "/") and (path.endswith("/../") or path.endswith("/"))):
        self.dirlisting(path)

      if (os.path.isdir(webroot + path)):
        self.movedtemp(path)
    	
      else:
        self.servefile(method, path)
	
  def badrequest(self):
    sys.stdout.write("HTTP/1.0 400\r\nPragma: no-cache\r\nContent-Type: text/html\r\nContent-Length: 112\r\n\r\n<HTML><HEAD><TITLE>Error</TITLE></HEAD>\r\n<BODY><CENTER><H2><BR><BR>400 : BAD REQUEST</H2></CENTER></BODY></HTML>")
    sys.stdout.flush()
    sys.exit(0)
	
  def dirlisting(self, path):
    date = time.strftime("Date: %a %b %d %H:%M %Y\r", time.gmtime(time.time()))
    splittedpath = re.findall(r'([^/]*/)', path)[1:]
    pathtolist = webroot + "/"
    for item in splittedpath:
      if (item != "/" and item != "../" and item != "./"):
        pathtolist += item
      else:
        pathtolist = webroot + "/"
        break
    entriesindir = [ "./", "../" ]
    for item in os.listdir(pathtolist):
      if (item.startswith("__")):
        continue
      if (os.path.isdir(pathtolist + item)):
        entriesindir.append(item + "/")
      else:
        entriesindir.append(item)
    if (len(splittedpath) < 2):
      updir = "/__FSys_Root"
    else:
      updir = "/" + "".join(splittedpath[:-1])
    sys.stdout.write("HTTP/1.0 200\r\nServer: HTTP-Server V1.27\r\nPragma: no-cache\r\nDate: " + date + "\r\nLast-Modified: " + date + "\r\nContent-Type: text/html\r\n\r\n<HTML><HEAD>\r\n<TITLE>Index of " + path + "</TITLE></HEAD>\r\n<BODY>\r\n<H1>Index of " + path + "</H1>\r\n<PRE>Name" + 36*" " + "Last modified" + 14*" " + "Size\r\n<BR><HR>\r\n\r\n<A HREF=\"" + updir + "\"><IMG ALIGN=absbottom BORDER=0 SRC=\"/SYS/MENU.GIF\" ALT=\"[DIR]\"></A>  <A HREF=\"" + updir + "\">Up to higher level directory</A>\r\n\r\n")

    for item in entriesindir:
      if (os.path.isdir(pathtolist + item)):
        sys.stdout.write("<A HREF=\"" + item + "\"><IMG ALIGN=absbottom BORDER=0 SRC=\"/SYS/MENU.GIF\" ALT=\"[DIR]\"></A>  <A HREF=\"" + item + "\">" + item + "</A>" + (35 - len(item))*" " + "Sat Jan  1 00:00 1994\r\n")
      else:
        f = file(pathtolist + item, 'r')
        length = 0
        for line in f.readlines():
          length += len(line)
        f.close()
        sys.stdout.write("<A HREF=\"" + item + "\"><IMG ALIGN=absbottom BORDER=0 SRC=\"/SYS/TEXT.GIF\" ALT=\"[File]\"></A>  <A HREF=\"" + item + "\">" + item + "</A>" + (35 - len(item))*" " + "Sat Jan  1 00:00 1994      " + str(length) + "\r\n")
    sys.stdout.write("</PRE></BODY></HTML>")
    sys.stdout.flush()
    sys.exit(0)
	
  def movedtemp(self, path):
    if (path == "/"):
      location = "/index.htm"
    else:
      location = path + "/"
  	
    sys.stdout.write("HTTP/1.0 302\r\nLocation: " + location + "\r\nPragma: no-cache\r\nContent-Type: text/html\r\nContent-Length: " + str(118 + len(path)) + "\r\n\r\n<HTML><HEAD><TITLE>Error</TITLE></HEAD>\r\n<BODY><CENTER><H2>" + path + "<BR><BR>302 : MOVED TEMPORARILY</H2></CENTER></BODY></HTML>")
    sys.stdout.flush()
    sys.exit(0)

  def notallowed(self, path):
    sys.stdout.write("HTTP/1.0 405\r\nAllow: GET, HEAD\r\nPragma: no-cache\r\nContent-Type: text/html\r\nContent-Length: " + str(119 + len(path)) + "\r\n\r\n<HTML><HEAD><TITLE>Error</TITLE></HEAD>\r\n<BODY><CENTER><H2>" + path + "<BR><BR>405 : METHOD NOT ALLOWED</H2></CENTER></BODY></HTML>")
    sys.stdout.flush()
    sys.exit(0)

  def notfound(self, path):
    sys.stdout.write("HTTP/1.0 404\r\nPragma: no-cache\r\nContent-Type: text/html\r\nContent-Length: " + str(110 + len(path)) + "\r\n\r\n<HTML><HEAD><TITLE>Error</TITLE></HEAD>\r\n<BODY><CENTER><H2>" + path + "<BR><BR>404 : NOT FOUND</H2></CENTER></BODY></HTML>")
    sys.stdout.flush()
    sys.exit(0)
	
  def servefile(self, method, path):
    date = time.strftime("Date: %a %b %d %H:%M %Y\r", time.gmtime(time.time()))
    if (path.endswith(".gif")):
      type = "image/gif"
    else:
      type = "text/html"
    f = file(webroot + path, 'r')
    filelines = f.readlines()
    f.close()
    length = 0
    for line in filelines:
      length += len(line)
    sys.stdout.write("HTTP/1.0 200\r\nServer: HTTP-Server V1.27\r\nDate: " + date + "\r\nLast-Modified: Sat Jan  1 00:00 1994\r\nContent-Type: " + type + "\r\nContent-Length: " + str(length) + "\r\n\r\n")
    if (method == "GET"):
      for line in filelines:
        sys.stdout.write(line)
    sys.stdout.flush()
    sys.exit(0)

  def testmail(self):
    sys.stdout.write("HTTP/1.0 401\r\nWWW-Authenticate: Basic realm=\"/__Send_Test_Mail\"\r\nPragma: no-cache\r\nContent-Type: text/html\r\nContent-Length: 130\r\n\r\n<HTML><HEAD><TITLE>Error</TITLE></HEAD>\r\n<BODY><CENTER><H2>/__Send_Test_Mail<BR><BR>401 : UNAUTHORIZED</H2></CENTER></BODY></HTML>")
    sys.stdout.flush()
    sys.exit(0)
	
  def unimplemented(self, path):
     sys.stdout.write("HTTP/1.0 501\r\nPragma: no-cache\r\nContent-Type: text/html\r\nContent-Length: 124\r\n\r\n<HTML><HEAD><TITLE>Error</TITLE></HEAD>\r\n<BODY><CENTER><H2>" + path + "<BR><BR>501 : NOT IMPLEMENTED</H2></CENTER></BODY></HTML>")
     sys.stdout.flush()
     sys.exit(0)

HTTPSim().run()
