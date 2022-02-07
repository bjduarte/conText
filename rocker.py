#!/usr/bin/python3

import re
import sys
import io
import os
import fnmatch
from tabnanny import check
import pandas as pandas


class RockerParse:

  def __init__(self):
    self.rexDict = {}
    self.path = ''

    p = ''
    for file in os.listdir('./convertedLogs'):
      if fnmatch.fnmatch(file, '*.txt'):
        self.path = p.join(("./convertedLogs/", file))

  def ReadFile(self, logFile):
    # initializing the lists to store the regular expressions
    systemTime = []
    zooloo = []
    date = []
    imsi = []
    imei = []
    tmsi = []
    lat = []
    long = []
    course = []
    speed= []
    alt = []
    cause = []
    tac = []
    ta = []
    gpsDate = []
    gpsTime = []

    # defining the regular expressions for each field
    SYSTEMTIME = re.compile(r'^\d{2}:\d{2}:\d{2}\s?')
    ZOOLOO = re.compile(r'\[\d{2}:\d{2}:\d{2}\]')
    DATE = re.compile(r'\[\d{8}\]')
    IMSI = re.compile(r'IMSI:[0-9]+:')
    IMEI = re.compile(r'IMEI:[0-9]+:')
    TMSI = re.compile(r'TMSI:0xF+:')
    LAT = re.compile(r'LAT:[NS][0-9]+\.[0-9]+:')
    LONG = re.compile(r'LONG:[EW][0-9]+\.[0-9]+:')
    COURSE = re.compile(r'COURSE:[0-9]+\.[0-9]+:')
    SPEED = re.compile(r'SPEED:[0-9]+\.[0-9]+:')
    ALT = re.compile(r'ALT:[A-Z][0-9]+\.[0-9]+:')
    CAUSE = re.compile(r'CAUSE:[0-9]+:')
    TAC = re.compile(r'TAC:\w+\s\w+\s\w+\s\w+:')
    TA = re.compile(r'TA:[0-9]+:[0-9A-Z]+:[0-9]+:')
    GPSDATE = re.compile(r'GPSDATE:\d{8}:')
    GPSTIME = re.compile(r'GPSTIME:[0-9]+\.[0-9]+:')

    try:
      with open(logFile, 'r') as fin:

        # reading each line of the file
        while True:
          line = fin.readline()

          # check to make sure the file has data
          if not line:
            fin.close()
            break
          else:
            # add all matches to a list
            systemTime.append(re.finditer(SYSTEMTIME, line))
            zooloo.append(re.finditer(ZOOLOO, line))
            date.append(re.finditer(DATE, line))
            imsi.append(re.finditer(IMSI, line))
            imei.append(re.finditer(IMEI, line))
            tmsi.append(re.finditer(TMSI, line))
            lat.append(re.finditer(LAT, line))
            long.append(re.finditer(LONG, line))
            course.append(re.finditer(COURSE, line))
            speed.append(re.finditer(SPEED, line))
            alt.append(re.finditer(ALT, line))
            cause.append(re.finditer(CAUSE, line))
            tac.append(re.finditer(TAC, line))
            ta.append(re.finditer(TA, line))
            gpsDate.append(re.finditer(GPSDATE, line))
            gpsTime.append(re.finditer(GPSTIME, line))

    except FileNotFoundError:
      print("File not found!")

    # adding all lists to the dictionary of fields
    self.rexDict = {
      'System Time': systemTime,
      'Zooloo Time': zooloo,
      'Date': date,
      'IMSI': imsi,
      'IMEI': imei,
      'TMSI': tmsi,
      'LAT': lat,
    'LONG': long,
    'COURSE': course,
    'SPEED': speed,
    'ALT': alt,
    'CAUSE': cause,
    'TAC': tac,
    'TA': ta,
    'GPS Date': gpsDate,
    'GPS Time': gpsTime
    }


  def printCapturedFields(self):

    for rexLists in self.rexDict.values():
      for matches in rexLists:
        for match in matches:
          print(      match.group())


  def CheckInput(self):

    a = len(self.rexDict.get('System Time'))
    b = len(self.rexDict.get('Zooloo Time'))
    c = len(self.rexDict.get('Date'))
    d = len(self.rexDict.get('IMSI'))
    e = len(self.rexDict.get('IMEI'))
    f = len(self.rexDict.get('TMSI'))
    g = len(self.rexDict.get('LAT'))
    h = len(self.rexDict.get('LONG'))
    i = len(self.rexDict.get('COURSE'))
    j = len(self.rexDict.get('SPEED'))
    k = len(self.rexDict.get('ALT'))
    l = len(self.rexDict.get('CAUSE'))
    m = len(self.rexDict.get('TAC'))
    n = len(self.rexDict.get('TA'))
    o = len(self.rexDict.get('GPS Date'))
    p = len(self.rexDict.get('GPS Time'))

    checklist = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]
    baseline = max(checklist)
    count = 0
    for datapoint in checklist:
      if datapoint != baseline:
        print('Data item at index: ',count, ': has the value of: ', datapoint, 'and the target is: ',baseline)
        break
      count +=1


  def extractValue(self):
    # method to extract the value of the match found in the reg ex
    pass



if __name__ == '__main__':
  print("Starting")
  rkr = RockerParse()
  inFile = rkr.path
  rkr.ReadFile(inFile)
  # rkr.printCapturedFields()
  rkr.CheckInput()
