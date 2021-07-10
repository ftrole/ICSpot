#!/usr/bin/env python

# honeyd-s7.py
#
# Copyright (C) 2006  Joel Arnold - EPFL & CERN
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

import struct, tpkt, cotp, s7, sys, pickle

MEMORY_FILE = "S7_MEMORY_STATE"

def receive_packet():
  tpkt_data = sys.stdin.read(4)
  if (tpkt_data == ''):
    return ''
  else:
    tpkt_fields = tpkt.tpkt().decode(tpkt_data)
    cotp_data = sys.stdin.read(tpkt_fields['length'] - 4)
    return cotp.cotp().decode(cotp_data)

def init_memory(filename):
  try:
    memfile = file(filename, 'r')
    memory = pickle.load(memfile)
    memfile.close()
    return memory
  except:
    from memory import memory
    return memory

def save_memory(memory, filename):
  memfile = file(filename, 'w')
  pickle.dump(memory, memfile)
  memfile.close()

def dump_memory_and_exit(memory, status):
  save_memory(memory, MEMORY_FILE)
  sys.exit(status)

memory = init_memory(MEMORY_FILE)

while True:
  try :
    cotp_fields = receive_packet()
  	
    if (cotp_fields == ''):
      dump_memory_and_exit(memory, 0)

    elif (cotp_fields['type'] == 'CR'):  	# CONNECTION REQUEST
    	# Prepare a connection confirm packet
      cotp_fields['type'] = 'CC'
      cotp_fields['dst_ref'] = cotp_fields['src_ref']
      cotp_fields['src_ref'] = 17457
      cotp_data = cotp.cotp().encode(cotp_fields)
      tpkt_data = tpkt.tpkt().encode(cotp_data)
    	# Send it
      sys.stdout.write(tpkt_data)
      sys.stdout.flush()	

    elif (cotp_fields['type'] == 'DT'):  	# DATA
      s7_fields = s7.s7().decode(cotp_fields['data'])
    	
      if (s7_fields['req_type'] == 240):	# PDU SIZE NEGOTIATION
        s7_fields['pdu_type'] = 3
        s7_fields['max'] = min(240, s7_fields['max'])
      	
        cotp_fields = { 'type' : 'DT' }
        cotp_fields['data'] = s7.s7().encode(s7_fields)
        cotp_data = cotp.cotp().encode(cotp_fields)
        tpkt_data = tpkt.tpkt().encode(cotp_data)
      	
        sys.stdout.write(tpkt_data)
        sys.stdout.flush()	
      	
      elif(s7_fields['req_type'] == 4):	# READ REQUEST
      	
        read_reqs = s7_fields['reads']
      	
        s7_fields = {
          'pdu_type'  :  3,
          'seq_nbr'  :  s7_fields['seq_nbr'],
          'req_type'  :  4,
          'nb_read'  :  s7_fields['nb_read']
          }
      	
        s7_fields['reads'] = []
      	
        for i in range(0, s7_fields['nb_read']):
          byte_count = read_reqs[i][0]
          source_id = read_reqs[i][1]
          source = read_reqs[i][2]
          address = read_reqs[i][3]
          if (not memory.has_key(source)):
          	#not available
            bit_count = 0
            data = struct.pack('BBBB', 10, 0, 0, 0)
            s7_fields['reads'].append([bit_count, data])
          elif (source == 33792):
            if (not memory[source].has_key(source_id)):
            	#not available
              bit_count = 0
              data = struct.pack('BBBB', 10, 0, 0, 0)
              s7_fields['reads'].append([bit_count, data])
            elif (address + byte_count > len(memory[source][source_id])):
            	#out of range
              bit_count = 0
              data = struct.pack('BBBB', 5, 0, 0, 0)
              s7_fields['reads'].append([bit_count, data])
            else:
            	#set the data accordingly
              bit_count = byte_count * 8
              data = ''
              for j in range(0, byte_count):
                data += struct.pack('B', memory[source][source_id][address + j])
              s7_fields['reads'].append([bit_count, data])
          elif (address + byte_count > len(memory[source])):
          	#out of range
            bit_count = 0
            data = struct.pack('BBBB', 5, 0, 0, 0)
            s7_fields['reads'].append([bit_count, data])
          else:
          	#set the data accordingly
            bit_count = byte_count * 8
            data = ''
            for j in range(0, byte_count):
              data += struct.pack('B', memory[source][address + j])
            s7_fields['reads'].append([bit_count, data])
      	
        cotp_fields = { 'type' : 'DT' }
        cotp_fields['data'] = s7.s7().encode(s7_fields)
        cotp_data = cotp.cotp().encode(cotp_fields)
        tpkt_data = tpkt.tpkt().encode(cotp_data)
      	
        sys.stdout.write(tpkt_data)
        sys.stdout.flush()	

      elif(s7_fields['req_type'] == 5):	# WRITE REQUEST
        write_reqs = s7_fields['writes']
        s7_fields = {
          'pdu_type'  :  3,
          'seq_nbr'  :  s7_fields['seq_nbr'],
          'req_type'  :  5,
          'nb_writes'  :  s7_fields['nb_writes']
          }
        s7_fields['writes'] = []
        for req in write_reqs:
          s7_fields['writes'].append(255)
      	
        cotp_fields = { 'type' : 'DT' }
        cotp_fields['data'] = s7.s7().encode(s7_fields)
        cotp_data = cotp.cotp().encode(cotp_fields)
        tpkt_data = tpkt.tpkt().encode(cotp_data)
      	
        sys.stdout.write(tpkt_data)
        sys.stdout.flush()	

      elif(s7_fields['req_type'] == 40):	# CPU START REQUEST
        s7_fields = {
          'pdu_type'  :  3,
          'seq_nbr'  :  s7_fields['seq_nbr'],
          'req_type'  :  s7_fields['req_type']
          }
        cotp_fields = { 'type' : 'DT' }
        cotp_fields['data'] = s7.s7().encode(s7_fields)
        cotp_data = cotp.cotp().encode(cotp_fields)
        tpkt_data = tpkt.tpkt().encode(cotp_data)
      	
        sys.stdout.write(tpkt_data)
        sys.stdout.flush()	
      	
    	
      elif(s7_fields['req_type'] == 41):	# CPU STOP REQUEST
        s7_fields = {
          'pdu_type'  :  3,
          'seq_nbr'  :  s7_fields['seq_nbr'],
          'req_type'  :  s7_fields['req_type']
          }
        cotp_fields = { 'type' : 'DT' }
        cotp_fields['data'] = s7.s7().encode(s7_fields)
        cotp_data = cotp.cotp().encode(cotp_fields)
        tpkt_data = tpkt.tpkt().encode(cotp_data)
      	
        sys.stdout.write(tpkt_data)
        sys.stdout.flush()	

      else:
        pass	
    	
  except:
    dump_memory_and_exit(memory, 0)
