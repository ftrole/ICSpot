#!/usr/bin/env python

# honeyd-modbus.py
#
# Copyright (C) 2006  Joel Arnold - EPFL & CERN
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

import sys, struct, array, string, math, pickle

class ModbusSim:
  """A class allowing the simulation of the modbus protocol of a PLC, to be used within Honeyd"""

  # Constants :
  MEMORY_FILE_BIT = "MODBUS_MEMORY_STATE_BIT"
  MEMORY_FILE_REG = "MODBUS_MEMORY_STATE_REG"
  BITMEMORYSIZE = 512
  REGMEMORYSIZE = 1024*16
  F1_MAXCOILS = 2000
  F2_MAXINPUTS = 2000
  F3_MAXREGISTERS = 125
  F4_MAXREGISTERS = 125
  F5_ZERO = 0
  F5_ONE = 65280
  F15_MAXCOILS = 1968
  F16_MAXREGISTERS = 123

  def run(self):
    """Starts the simulator"""
  	
    self.bitmemory = ModbusMem(self.BITMEMORYSIZE, self.MEMORY_FILE_BIT)
    self.regmemory = ModbusMem(self.REGMEMORYSIZE, self.MEMORY_FILE_REG)
  	
    while True:
      self.parseInput()
	
  def parseInput(self):
    """Get the input and send it to the next stage"""
  	
  	# Read the first 6 bytes (byte 4 and 5 contain the remaining length)
    tempQuery = sys.stdin.read(6)
    if (not(len(tempQuery) < 6)):
      tempQueryBytes = array.array('B', tempQuery)
      remainingLength = self.getWord(tempQueryBytes[4], tempQueryBytes[5])
    	
    	# Read the remaining bytes
      rawQuery = tempQuery + sys.stdin.read(remainingLength)
    	
      requestBytes = array.array('B', rawQuery)
    	
      self.transactionID = self.getWord(requestBytes[0], requestBytes[1])
      self.protocolID = self.getWord(requestBytes[2], requestBytes[3])
      self.length = self.getWord(requestBytes[4], requestBytes[5])
      self.unitID = requestBytes[6]
      self.functionCode = requestBytes[7]
      self.data = requestBytes[8:]
      self.exception = 0
    	
      if (self.protocolID != 0):
        sys.exit(0)
      else:
        self.createResponse()
    else:
      sys.exit(0)
	
  def getWord(self, byte0, byte1):
    """Returns the integer value of the combination of two bytes in big endian mode"""
  	
    return byte0*256 + byte1
  	
  def createResponse(self):
    """Creates the response and send it to the next stage"""
  	
    if self.functionCode == 1:
      """Read Coil Status"""
      bitAddress = self.getWord(self.data[0], self.data[1])
      bitCount = self.getWord(self.data[2], self.data[3])
      if ((bitCount < 1) or (bitCount > self.F1_MAXCOILS)):
        self.exception = 3
      elif ((bitAddress + bitCount) >= self.bitmemory.getSize()):
        self.exception = 2
      else:
        self.length = int(3 + math.ceil(bitCount/8.0))
        self.data = [ int(math.ceil(bitCount/8.0)) ]
        self.data.extend(self.bitmemory.getBytes(bitAddress, bitCount))
  	
    elif self.functionCode == 2:
      """Read Input Status"""
      bitAddress = self.getWord(self.data[0], self.data[1])
      bitCount = self.getWord(self.data[2], self.data[3])
      if ((bitCount < 1) or (bitCount > self.F2_MAXINPUTS)):
        self.exception = 3
      elif ((bitAddress + bitCount) >= self.bitmemory.getSize()):
        self.exception = 2
      else:
        self.length = int(3 + math.ceil(bitCount/8.0))
        self.data = [ int(math.ceil(bitCount/8.0)) ]
        self.data.extend(self.bitmemory.getBytes(bitAddress, bitCount))
  	
    elif self.functionCode == 3:
      """Read Holding Registers"""
      bitAddress = self.getWord(self.data[0], self.data[1])
      regCount = self.getWord(self.data[2], self.data[3])
      if ((regCount < 1) or (regCount > self.F3_MAXREGISTERS)):
        self.exception = 3
      elif ((bitAddress + regCount*16) >= self.regmemory.getSize()):
        self.exception = 2
      else:
        self.length = int(3 + regCount*2)
        self.data = [ regCount*2 ]
        self.data.extend(self.regmemory.getRegisters(bitAddress, regCount))
  	
    elif self.functionCode == 4:
      """Read Input Registers"""
      bitAddress = self.getWord(self.data[0], self.data[1])
      regCount = self.getWord(self.data[2], self.data[3])
      if ((regCount < 1) or (regCount > self.F4_MAXREGISTERS)):
        self.exception = 3
      elif ((bitAddress >= self.regmemory.getSize()) or ((bitAddress + regCount*16) >= self.regmemory.getSize())):
        self.exception = 2
      else:
        self.length = int(3 + regCount*2)
        self.data = [ regCount*2 ]
        self.data.extend(self.regmemory.getRegisters(bitAddress, regCount))
  	
    elif self.functionCode == 5:
      """Write Coil"""
      bitAddress = self.getWord(self.data[0], self.data[1])
      bitValue = self.getWord(self.data[2], self.data[3])
      if ((bitValue != self.F5_ZERO) and (bitValue != self.F5_ONE)):
        self.exception = 3
      elif (bitAddress >= self.bitmemory.getSize()):
        self.exception = 2
      else:
        self.length = 6
        if (bitValue == self.F5_ZERO):
          self.bitmemory.setBit(bitAddress, 0)
          self.data = [ self.data[0], self.data[1], self.F5_ZERO/256, self.F5_ZERO%256 ]
        else:
          self.bitmemory.setBit(bitAddress, 1)
          self.data = [ self.data[0], self.data[1], self.F5_ONE/256, self.F5_ONE%256 ]
        self.bitmemory.backupdata()
  	
    elif self.functionCode == 6:
      """Write Single Register"""
      bitAddress = self.getWord(self.data[0], self.data[1])
      regValue = self.getWord(self.data[2], self.data[3])
      if ((regValue < 0) or (regValue > 65535)):
        self.exception = 3
      elif ((bitAddress + 16) >= self.regmemory.getSize()):
        self.exception = 2
      else:
        self.length = 6
        self.regmemory.setRegister(bitAddress, regValue)
        self.data = self.data[0:4]
        self.regmemory.backupdata()
  	
    elif self.functionCode == 7:
      """Read Exception Status"""
      self.exception = 1
  	
    elif self.functionCode == 8:
      """Diagnostics"""
      self.exception = 1

    elif self.functionCode == 11:
      """Fetch Comm Event Counter"""
      self.exception = 1

    elif self.exception == 12:
      """Fetch Comm Event Log"""
      self.exception = 1
  	
    elif self.functionCode == 15:
      """Force Multiple Coils"""
      bitAddress = self.getWord(self.data[0], self.data[1])
      bitCount = self.getWord(self.data[2], self.data[3])
      byteCount = self.data[4]
      bitValues = self.data[5:]
      if ((bitCount < 1) or (bitCount > self.F15_MAXCOILS) or (math.ceil(bitCount/8.0) != byteCount)):
        self.exception = 3
      elif ((bitAddress + bitCount) >= self.bitmemory.getSize()):
        self.exception = 2
      else:
        self.length = 6
        self.bitmemory.setBits(bitAddress, bitCount, bitValues)
        self.data = self.data[0:4]
        self.bitmemory.backupdata()
  	
    elif self.functionCode == 16:
      """Write Multiple Registers"""
      bitAddress = self.getWord(self.data[0], self.data[1])
      regCount = self.getWord(self.data[2], self.data[3])
      byteCount = self.data[4]
      byteValues = self.data[5:]
      if ((regCount < 1) or (regCount > self.F16_MAXREGISTERS) or (byteCount != regCount*2)):
        self.exception = 2
      elif ((bitAddress + regCount*16) >= self.regmemory.getSize()):
        self.exception = 3
      else:
        self.length = 6
        regValues = []
        for i in range(0, regCount):
          regValues.append(int(256*byteValues[2*i] + byteValues[2*i + 1]))
        self.regmemory.setRegisters(bitAddress, regCount, regValues)
        self.data = self.data[0:4]
        self.regmemory.backupdata()
  	
    elif self.functionCode == 17:
      """Report Slave ID"""
      self.exception = 1
  	
    elif self.functionCode == 20:
      """Read General Reference"""
      self.exception = 1

    elif self.functionCode == 21:
      """Write General Reference"""
      self.exception = 1

    elif self.functionCode == 22:
      """Mask Write 4X Register"""
      self.exception = 1

    elif self.functionCode == 23:
      """Read/Write 4X Registers"""
      self.exception = 1

    elif self.functionCode == 24:
      """Read FIFO Queue"""
      self.exception = 1
  	
    else:
      """Unknown Function Code"""
      self.exception = 1

    if (self.exception != 0):
      self.length = 3
      self.functionCode += 128
      self.data = [self.exception]

    self.sendResponse()
	
  def sendResponse(self):
    """Send the response back"""
  	
    response = [ self.transactionID, self.protocolID, self.length, self.unitID, self.functionCode ]
    response.extend(self.data)
    rawResponse = struct.pack('!HHHBB' + str(self.length - 2) + 'B', *response)
	
    sys.stdout.write(rawResponse)
    sys.stdout.flush()

class ModbusMem:
  """This class simulates the memory space of a plc. It is bit - addressed"""

  def __init__(self, bitSize, filename):
    """Constructor. Initializes all bits to zero"""
  	
    self.size = bitSize
    self.file = file
    self.filename = filename
    try:
      datafile = file(self.filename, 'r')
      self.data = pickle.load(datafile)
      datafile.close()
    except:
      self.data = []
      for i in range(bitSize):
        self.data.append(False)

  def backupdata(self):
    """Saves the memory to the filename given at initialization"""
    datafile = file(self.filename, 'w')
    pickle.dump(self.data, datafile)
    datafile.close()

  def getBytes(self, bitAddress, bitCount):
    currentStart = bitAddress
    remainingBits = bitCount
    bytes = []
    while (remainingBits >= 8):
      bytes.append(self.getByte(currentStart))
      currentStart += 8
      remainingBits -= 8
    if (remainingBits > 0):
      temp = 0
      for i in range(remainingBits):
        temp += self.getBit(currentStart + i) * math.pow(2, i)
      bytes.append(int(temp))
    return bytes

  def getByte(self, bitAddress):
    temp = 0
    for i in range(8):
      temp += self.getBit(bitAddress + i) * math.pow(2, i)
    return int(temp)

  def getBit(self, bitAddress):
    if (self.data[bitAddress]):
      return 1
    else:
      return 0

  def setBit(self, bitAddress, bitState):
    if (bitState == 1):
      self.data[bitAddress] = True
    else:
      self.data[bitAddress] = False

  def getSize(self):
    return self.size

  def getRegisters(self, bitAddress, regCount):
    currentStart = bitAddress
    remainingRegs = regCount
    registers = []
    while (remainingRegs > 0):
      registers.append(self.getByte(currentStart + 8))
      registers.append(self.getByte(currentStart))
      currentStart += 16
      remainingRegs -= 1
    return registers

  def setRegister(self, bitAddress, regValue):
    self.setByte(bitAddress, regValue%256)
    self.setByte(bitAddress + 8, regValue/256)

  def setRegisters(self, bitAddress, regCount, regValues):
    for i in range(regCount):
      self.setRegister(bitAddress + 16*i, regValues[i])

  def setBits(self, bitAddress, bitCount, bitValues):
    remainingBits = bitCount
    for i in range(bitCount/8):
      self.setByte(bitAddress + i*8, bitValues[i])
      remainingBits -= 8
    if (remainingBits > 0):
      tempByteValue = bitValues[bitCount/8]
      for i in range(remainingBits - 1, -1, -1):
        if (tempByteValue >= math.pow(2, i)):
          self.setBit(bitAddress + i, 1)
          tempByteValue -= math.pow(2, i)
        else:
          self.setBit(bitAddress + i, 0)
        if (tempByteValue != 0):
          raise Exception("Invalid byte value :: setBits")
    	

  def setByte(self, bitAddress, byteValue):
    tempByteValue = byteValue
    for i in range(7, -1, -1):
      if (tempByteValue >= math.pow(2, i)):
        self.setBit(bitAddress + i, 1)
        tempByteValue -= math.pow(2, i)
      else:
        self.setBit(bitAddress + i, 0)
    if (tempByteValue != 0):
      raise Exception("Invalid byte value :: setByte")

  	
ModbusSim().run()
