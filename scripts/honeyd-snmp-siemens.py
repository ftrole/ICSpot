#!/usr/bin/env python

# honeyd-snmp-siemens.py
#
# Copyright (C) 2006  Joel Arnold - EPFL & CERN
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

import struct, v1, sys, array, re, asn1, os

typemap = {
  'STRING'    : 'OCTETSTRING',
  'OID'       : 'OBJECTID',
  'INTEGER'   : 'INTEGER',
  'Timeticks' : 'TIMETICKS',
  'Counter32' : 'COUNTER32',
  'Gauge32'   : 'GAUGE32',
  'IpAddress' : 'IPADDRESS'
  }

ip_address = os.environ['HONEYD_IP_DST']
net_address = re.sub(r'(\d+\.\d+)\.\d+\.\d+', r'\1.0.0', ip_address)

data = [
  '.1.3.6.1.2.1.1.1.0 = STRING: Siemens, SIMATIC, S7-300',
  '.1.3.6.1.2.1.1.2.0 = OID: .0.0',
  '.1.3.6.1.2.1.1.3.0 = Timeticks: 181165360',
  '.1.3.6.1.2.1.1.4.0 = STRING:',
  '.1.3.6.1.2.1.1.5.0 = STRING:',
  '.1.3.6.1.2.1.1.6.0 = STRING:',
  '.1.3.6.1.2.1.1.7.0 = INTEGER: 72',
  '.1.3.6.1.2.1.2.1.0 = INTEGER: 1',
  '.1.3.6.1.2.1.2.2.1.1.1 = INTEGER: 1',
  '.1.3.6.1.2.1.2.2.1.2.1 = STRING: Siemens, SIMATIC NET, CP343-1 IT, 6GK7 343-1GX20-0XE0, HW: Version 1, FW: Version V1.1.4, Fast Ethernet Port 1, Rack 0, Slot 4, 100 Mbit, full duplex, autonegotiation',
  '.1.3.6.1.2.1.2.2.1.3.1 = INTEGER: 6',
  '.1.3.6.1.2.1.2.2.1.4.1 = INTEGER: 1500',
  '.1.3.6.1.2.1.2.2.1.5.1 = Gauge32: 100000000',
  '.1.3.6.1.2.1.2.2.1.6.1 = STRING: 8:0:6:72:7c:8',
  '.1.3.6.1.2.1.2.2.1.7.1 = INTEGER: 1',
  '.1.3.6.1.2.1.2.2.1.8.1 = INTEGER: 1',
  '.1.3.6.1.2.1.2.2.1.9.1 = Timeticks: 2448580',
  '.1.3.6.1.2.1.2.2.1.10.1 = Counter32: 83436854',
  '.1.3.6.1.2.1.2.2.1.11.1 = Counter32: 445126',
  '.1.3.6.1.2.1.2.2.1.12.1 = Counter32: 822805',
  '.1.3.6.1.2.1.2.2.1.13.1 = Counter32: 0',
  '.1.3.6.1.2.1.2.2.1.14.1 = Counter32: 0',
  '.1.3.6.1.2.1.2.2.1.15.1 = Counter32: 0',
  '.1.3.6.1.2.1.2.2.1.16.1 = Counter32: 25980254',
  '.1.3.6.1.2.1.2.2.1.17.1 = Counter32: 303652',
  '.1.3.6.1.2.1.2.2.1.18.1 = Counter32: 111',
  '.1.3.6.1.2.1.2.2.1.19.1 = Counter32: 0',
  '.1.3.6.1.2.1.2.2.1.20.1 = Counter32: 0',
  '.1.3.6.1.2.1.2.2.1.21.1 = Gauge32: 1',
  '.1.3.6.1.2.1.2.2.1.22.1 = OID: .0.0',
  '.1.3.6.1.2.1.4.1.0 = INTEGER: 2',
  '.1.3.6.1.2.1.4.2.0 = INTEGER: 60',
  '.1.3.6.1.2.1.4.3.0 = Counter32: 446094',
  '.1.3.6.1.2.1.4.4.0 = Counter32: 221',
  '.1.3.6.1.2.1.4.5.0 = Counter32: 0',
  '.1.3.6.1.2.1.4.6.0 = Counter32: 0',
  '.1.3.6.1.2.1.4.7.0 = Counter32: 0',
  '.1.3.6.1.2.1.4.8.0 = Counter32: 0',
  '.1.3.6.1.2.1.4.9.0 = Counter32: 445572',
  '.1.3.6.1.2.1.4.10.0 = Counter32: 312618',
  '.1.3.6.1.2.1.4.11.0 = Counter32: 0',
  '.1.3.6.1.2.1.4.12.0 = Counter32: 0',
  '.1.3.6.1.2.1.4.13.0 = INTEGER: 60',
  '.1.3.6.1.2.1.4.14.0 = Counter32: 455',
  '.1.3.6.1.2.1.4.15.0 = Counter32: 151',
  '.1.3.6.1.2.1.4.16.0 = Counter32: 1',
  '.1.3.6.1.2.1.4.17.0 = Counter32: 0',
  '.1.3.6.1.2.1.4.18.0 = Counter32: 0',
  '.1.3.6.1.2.1.4.19.0 = Counter32: 0',
  '.1.3.6.1.2.1.4.20.1.1.' + ip_address + ' = IpAddress: ' + ip_address,
  '.1.3.6.1.2.1.4.20.1.2.' + ip_address + ' = INTEGER: 1',
  '.1.3.6.1.2.1.4.20.1.3.' + ip_address + ' = IpAddress: ' + net_address,
  '.1.3.6.1.2.1.4.20.1.4.' + ip_address + ' = INTEGER: 1',
  '.1.3.6.1.2.1.4.20.1.5.' + ip_address + ' = INTEGER: 65528',
  '.1.3.6.1.2.1.4.21.1.1.' + net_address + ' = IpAddress: ' + net_address,
  '.1.3.6.1.2.1.4.21.1.2.' + net_address + ' = INTEGER: 1',
  '.1.3.6.1.2.1.4.21.1.3.' + net_address + ' = INTEGER: 1',
  '.1.3.6.1.2.1.4.21.1.4.' + net_address + ' = INTEGER: -1',
  '.1.3.6.1.2.1.4.21.1.5.' + net_address + ' = INTEGER: -1',
  '.1.3.6.1.2.1.4.21.1.6.' + net_address + ' = INTEGER: -1',
  '.1.3.6.1.2.1.4.21.1.7.' + net_address + ' = IpAddress: ' + ip_address,
  '.1.3.6.1.2.1.4.21.1.8.' + net_address + ' = INTEGER: 3',
  '.1.3.6.1.2.1.4.21.1.9.' + net_address + ' = INTEGER: 2',
  '.1.3.6.1.2.1.4.21.1.10.' + net_address + ' = INTEGER: 1809982',
  '.1.3.6.1.2.1.4.21.1.11.' + net_address + ' = IpAddress: 255.255.0.0',
  '.1.3.6.1.2.1.4.21.1.12.' + net_address + ' = INTEGER: -1',
  '.1.3.6.1.2.1.4.21.1.13.' + net_address + ' = OID: .0.0',
  '.1.3.6.1.2.1.4.23.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.1.0 = Counter32: 3674',
  '.1.3.6.1.2.1.5.2.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.3.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.4.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.5.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.6.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.7.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.8.0 = Counter32: 87',
  '.1.3.6.1.2.1.5.9.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.10.0 = Counter32: 4',
  '.1.3.6.1.2.1.5.11.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.12.0 = Counter32: 12',
  '.1.3.6.1.2.1.5.13.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.14.0 = Counter32: 376',
  '.1.3.6.1.2.1.5.15.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.16.0 = Counter32: 262',
  '.1.3.6.1.2.1.5.17.0 = Counter32: 1',
  '.1.3.6.1.2.1.5.18.0 = Counter32: 20',
  '.1.3.6.1.2.1.5.19.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.20.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.21.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.22.0 = Counter32: 87',
  '.1.3.6.1.2.1.5.23.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.24.0 = Counter32: 4',
  '.1.3.6.1.2.1.5.25.0 = Counter32: 0',
  '.1.3.6.1.2.1.5.26.0 = Counter32: 0',
  '.1.3.6.1.2.1.6.1.0 = INTEGER: 2',
  '.1.3.6.1.2.1.6.2.0 = INTEGER: 0',
  '.1.3.6.1.2.1.6.3.0 = INTEGER: 100',
  '.1.3.6.1.2.1.6.4.0 = INTEGER: -1',
  '.1.3.6.1.2.1.6.5.0 = Counter32: 0',
  '.1.3.6.1.2.1.6.6.0 = Counter32: 9059',
  '.1.3.6.1.2.1.6.7.0 = Counter32: 93',
  '.1.3.6.1.2.1.6.8.0 = Counter32: 317',
  '.1.3.6.1.2.1.6.9.0 = Gauge32: 0',
  '.1.3.6.1.2.1.6.10.0 = Counter32: 305161',
  '.1.3.6.1.2.1.6.11.0 = Counter32: 311164',
  '.1.3.6.1.2.1.6.12.0 = Counter32: 30',
  '.1.3.6.1.2.1.6.13.1.1.' + ip_address + '.102.0.0.0.0.0 = INTEGER: 2',
  '.1.3.6.1.2.1.6.13.1.1.' + ip_address + '.80.0.0.0.0.0 = INTEGER: 2',
  '.1.3.6.1.2.1.6.13.1.1.' + ip_address + '.21.0.0.0.0.0 = INTEGER: 2'
  ]


try:
  payload = sys.stdin.read(2)
  length = struct.unpack('BB', payload)[1]
  payload += sys.stdin.read(length)
  (object, rest) = v1.decode(payload)
	
  community = object.get('community', 'nil')
  if (community not in [ 'public', 'private' ]):
    sys.exit(0)

  request_type = object.get('tag', 'nil')

  # GET
  if (request_type == "GETREQUEST"):
    oids = map(asn1.OBJECTID().decode, object.get('encoded_oids', 'nil'))
    vals = []
    for i in range(0, len(oids)):
      oid = oids[i]
      acc = oid[0]
      original_oid = acc
      match = False
      matched = ''
      for j in range(0, len(data)):
        if re.match(acc, data[j]):
          match = True
          matched = data[j]
          break
      if match:
        indatafile, type, value = re.match('\s*(\S+)\s*=\s*(\S+):\s*(.*)\s*$', matched).groups()
        type = typemap[type]
        if (type in ['INTEGER', 'TIMETICKS', 'COUNTER32', 'GAUGE32']):
          value = int(value)
        if (indatafile == original_oid):
          vals.append(eval('asn1.' + type + '()').encode(value))
      else:
        resp = object.reply()
        encoded = resp.encode(tag='GETRESPONSE', error_status=2, error_index=i+1)
        sys.stdout.write(encoded)
        sys.stdout.flush()
        sys.exit(0)
    if match:
      resp = object.reply()
      encoded = resp.encode(tag='GETRESPONSE', encoded_vals=vals)
      sys.stdout.write(encoded)
      sys.stdout.flush()
      sys.exit(0)
  	
  # GETNEXT
  elif (request_type == "GETNEXTREQUEST"):
    oids = map(asn1.OBJECTID().decode, object.get('encoded_oids', 'nil'))
    noids = []
    vals = []
    for i in range(0, len(oids)):
      oid = oids[i]
      acc = oid[0]
      original_oid = acc
      match = False
      matched = ''
      first_try = True
      indatafile = type = value = ''
	
      for j in range(0, len(data)):
        fileoid = re.match('^\s*(\S+)', data[j]).group(1)
        if ((fileoid == original_oid) and (j < len(data)-1)):
          match = True
          matched = data[j+1]
          break
      while (not match):
        acc = re.match('((\.\d+)*)\.\d+', acc).group(1)
        for k in range(0, len(data)):
          if (re.match(acc, data[k])):
            match = True
            matched = data[k]
            break
      indatafile, type, value = re.match('\s*(\S+)\s*=\s*(\S+):\s*(.*)\s*$', matched).groups()
      type = typemap[type]
      if (type in ['INTEGER', 'TIMETICKS', 'COUNTER32', 'GAUGE32']):
        value = int(value)
      noids.append(asn1.OBJECTID().encode(indatafile))
      vals.append(eval('asn1.' + type + '()').encode(value))
    resp = object.reply()
    encoded = resp.encode(tag='GETRESPONSE', encoded_oids=noids, encoded_vals=vals)
    sys.stdout.write(encoded)
    sys.stdout.flush()
    sys.exit(0)
	
  elif ((request_type == "SETREQUEST") and (community == 'private') and (len(object.get('encoded_oids', 'nil')) == 1)):
    resp = object.reply()
    encoded = resp.encode(tag='GETRESPONSE', error_status=2, error_index=1)
    sys.stdout.write(encoded)
    sys.stdout.flush()
    sys.exit(0)

except:
  sys.exit(0)
