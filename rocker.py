#!/usr/bin/python3

import re
import sys
import io
import os
import fnmatch
import pandas as pandas


class RockerParse:

  def __init__(self):
    self.rexDict = {}
    self.systemTime = []
    self.zooloo = []
    self.date = []
    self.IMSI = []
    self.IMEI = []
    self.TMSI = []
    self.LAT = []
    self.LONG = []
    self.COURSE = []
    self.SPEED = []
    self.ALT = []
    self.CAUSE = []
    self.TAC = []
    self.TA = []
    self.GPSDATE = []
    self.GPSTIME = []

    self.path = ''

    p = ''
    for file in os.listdir('./convertedLogs'):
      if fnmatch.fnmatch(file, '*.txt'):
        self.path = p.join(("./convertedLogs/", file))

  def ReadFile(self, logFile):
    try:
      with open(logFile, 'r') as fin:

        while True:
          line = fin.readline()

          if not line:
            fin.close()
            break
          else:

            systemTime = re.finditer(r'^\d{2}:\d{2}:\d{2}\s?', line)
            self.systemTime.append(systemTime)
            zooloo = re.finditer(r'\[\d{2}:\d{2}:\d{2}\]', line)
            self.zooloo.append(zooloo)
            date = re.finditer(r'\[\d{8}\]', line)
            self.date.append(date)
            IMSI = re.finditer(r'IMSI:[0-9]+:', line)
            self.IMSI.append(IMSI)
            IMEI = re.finditer(r'IMEI:[0-9]+:', line)
            self.IMEI.append(IMEI)
            TMSI = re.finditer(r'TMSI:0xF+:', line)
            self.TMSI.append(TMSI)
            LAT = re.finditer(r'LAT:[NS][0-9]+\.[0-9]+:', line)
            self.LAT.append(LAT)
            LONG = re.finditer(r'LONG:[EW][0-9]+\.[0-9]+:', line)
            self.LONG.append(LONG)
            COURSE = re.finditer(r'COURSE:[0-9]+\.[0-9]+:', line)
            self.COURSE.append(COURSE)
            SPEED = re.finditer(r'SPEED:[0-9]+\.[0-9]+:', line)
            self.SPEED.append(SPEED)
            ALT = re.finditer(r'ALT:[A-Z][0-9]+\.[0-9]+:', line)
            self.ALT.append(ALT)
            CAUSE = re.finditer(r'CAUSE:[0-9]+:', line)
            self.CAUSE.append(CAUSE)
            TAC = re.finditer(r'TAC:\w+\s\w+\s\w+\s\w+:', line)
            self.TAC.append(TAC)
            TA = re.finditer(r'TA:[0-9]+:[0-9A-Z]+:[0-9]+:', line)
            self.TA.append(TA)
            GPSDATE = re.finditer(r'GPSDATE:\d{8}:', line)
            self.GPSDATE.append(GPSDATE)
            GPSTIME = re.finditer(r'GPSTIME:[0-9]+\.[0-9]+:', line)
            self.GPSTIME.append(GPSTIME)

    except FileNotFoundError:
      print("File not found!")

    self.rexDict = {
      'System Time': self.systemTime,
      'Zooloo Time': self.zooloo,
      'Date': self.date,
      'IMSI': self.IMSI,
      'IMEI': self.IMEI,
      'TMSI': self.TMSI,
      'LAT': self.LAT,
    'LONG': self.LONG,
    'COURSE': self.COURSE,
    'SPEED': self.SPEED,
    'ALT': self.ALT,
    'CAUSE': self.CAUSE,
    'TAC': self.TAC,
    'TA': self.TA,
    'GPSDATE': self.GPSDATE,
    'GPSTIME': self.GPSTIME
    }


  def WriteData(self):

    for key, rx in self.rexDict.items():
      print(type(rx))


      # print(match.group())
    # for match in self.zooloo:
    #   print('Zooloo Time: ', match.group())
    # for match in self.date:
    #   print('Date: ', match.group())
    # for match in self.IMSI:
    #   print(match.group())
    # for match in self.IMEI:
    #   print(match.group())
    # for match in self.TMSI:
    #   print(match.group())
    # for match in self.LAT:
    #   print(match.group())
    # for match in self.LONG:
    #   print(match.group())
    # for match in self.COURSE:
    #   print(match.group())
    # for match in self.SPEED:
    #   print(match.group())
    # for match in self.ALT:
    #   print(match.group())
    # for match in self.CAUSE:
    #   print(match.group())
    # for match in self.TAC:
    #   print(match.group())
    # for match in self.TA:
    #   print(match.group())
    # for match in self.GPSDATE:
    #   print(match.group())
    # for match in self.GPSTIME:
    #   print(match.group())


  def CheckInput(self):

    a = len(self.systemTime)
    b = len(self.zooloo)
    c = len(self.date)
    d = len(self.IMSI)
    e = len(self.IMEI)
    f = len(self.TMSI)
    g = len(self.LAT)
    h = len(self.LONG)
    i = len(self.COURSE)
    j = len(self.SPEED)
    k = len(self.ALT)
    l = len(self.CAUSE)
    m = len(self.TAC)
    n = len(self.TA)
    o = len(self.GPSDATE)
    p = len(self.GPSTIME)

    testPoint = 2
    checklist = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, testPoint]


    baseline = max(checklist)
    count = 0
    for datapoint in checklist:
      if datapoint != baseline:
        print('Data item at index: ',count, ': has the value of: ', datapoint, 'and the target is: ',baseline)
        break
      count +=1

      






if __name__ == '__main__':
  print("Starting")
  rkr = RockerParse()
  inFile = rkr.path
  rkr.ReadFile(inFile)
  rkr.WriteData()
  # rkr.CheckInput()
