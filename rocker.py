#!/usr/bin/python3

import re
from readline import read_init_file
from shutil import ReadError
import sys
import io
import os
import fnmatch
import datetime
import time
import json

from pandas import read_feather


class RockerParse:

  def __init__(self):
    self.rawDict = {}
    self.striptDict = {}
    self.path = ''

    # defining the regular expressions for each field
    self.SYSTEMTIME = re.compile(r'(?P<SystemTimeValue>^\d{2}:\d{2}:\d{2})\s?')
    self.ZOOLOO = re.compile(r'\[(?P<ZoolooTimeValue>\d{2}:\d{2}:\d{2})\]')
    self.DATE = re.compile(r'\[(?P<DateValue>\d{8})\]')
    self.IMSI = re.compile(r'IMSI:(?P<IMSIValue>[0-9]+):')
    self.IMEI = re.compile(r'IMEI:(?P<IMEIValue>[0-9]+):')
    self.TMSI = re.compile(r'TMSI:(?P<TMSIValue>0xF+):')
    self.LAT = re.compile(r'LAT:(?P<LatValue>[NS][0-9]+\.[0-9]+):')
    self.LONG = re.compile(r'LONG:(?P<LongValue>[EW][0-9]+\.[0-9]+):')
    self.COURSE = re.compile(r'COURSE:(?P<CourseValue>[0-9]+\.[0-9]+):')
    self.SPEED = re.compile(r'SPEED:(?P<SpeedValue>[0-9]+\.[0-9]+):')
    self.ALT = re.compile(r'ALT:(?P<AltValue>[A-Z][0-9]+\.[0-9]+):')
    self.CAUSE = re.compile(r'CAUSE:(?P<CauseValue>[0-9]+):')
    self.TAC = re.compile(r'TAC:(?P<TacValue>\w+\s\w+\s\w+\s\w+):')
    self.TA = re.compile(r'TA:(?P<TaValue>[0-9]+:[0-9A-Z]+:[0-9]+):')
    self.GPSDATE = re.compile(r'GPSDATE:(?P<GPSDateValue>\d{8}):')
    self.GPSTIME = re.compile(r'GPSTIME:(?P<GPSTimeValue>[0-9]+\.[0-9]+):')

    # capturing all the files for reading and parsing
    p = ''
    for file in os.listdir('./convertedLogs'):
      if fnmatch.fnmatch(file, '*.txt'):
        self.path = p.join(("./convertedLogs/", file))

  
  def ReadFile(self, logFile):

    try:
      with open(logFile, 'r') as fin:
        line = fin.readline()

        if not line:
          fin.close()()
        else:
          return line

    except FileNotFoundError:
      print("File not found!")


  def BuildRegExDictionaries(self, line):
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

    while line:

    # add all matches to a list
      systemTimeMatch = re.search(self.SYSTEMTIME, line)
      if systemTimeMatch == None:
        systemTime.append('None:')
      else:
        systemTime.append(systemTimeMatch.group(1))

      zoolooTimeMatch = re.search(self.ZOOLOO, line)
      if zoolooTimeMatch == None:
       zooloo.append('None:')
      else:
        zooloo.append(zoolooTimeMatch.group(1))

      dateMatch = re.search(self.DATE, line)
      if dateMatch == None:
        date.append('None:')
      else:
        date.append(dateMatch.group(1))

      imsiMatch = re.search(self.IMSI, line)
      if imsiMatch == None:
        imsi.append('None:')
      else:
        imsi.append(imsiMatch.group(1))

      imeiMatch = re.search(self.IMEI, line)
      if imeiMatch == None:
        imei.append('None:')
      else:
        imei.append(imeiMatch.group(1))

      tmsiMatch = re.search(self.TMSI, line)
      if tmsiMatch == None:
        tmsi.append('None:')
      else:
        tmsi.append(tmsiMatch.group(1))

      latMatch = re.search(self.LAT, line)
      if latMatch == None:
        lat.append('None:')
      else:
        lat.append(latMatch.group(1))

      longMatch = re.search(self.LONG, line)
      if longMatch == None:
        long.append('None:')
      else:
        long.append(longMatch.group(1))

      courseMatch = re.search(self.COURSE, line)
      if courseMatch == None:
        course.append('None:')
      else:
        course.append(courseMatch.group(1))

      speedMatch = re.search(self.SPEED, line)
      if speedMatch == None:
        speed.append('None:')
      else:
        speed.append(speedMatch.group(1))

      altMatch = re.search(self.ALT, line)
      if altMatch == None:
        alt.append('None:')
      else:
        alt.append(altMatch.group(1))

      causeMatch = re.search(self.CAUSE, line)
      if causeMatch == None:
        cause.append('None:')
      else:
        cause.append(causeMatch.group(1))

      tacMatch = re.search(self.TAC, line)
      if tacMatch == None:
        tac.append('None:')
      else:
        tac.append(tacMatch.group(1))

      taMatch = re.search(self.TA, line)
      if taMatch == None:
        ta.append('None:')
      else:
        ta.append(taMatch.group(1))

      gpsDateMatch = re.search(self.GPSDATE, line)
      if gpsDateMatch == None:
        gpsDate.append('None:')
      else:
        gpsDate.append(gpsDateMatch.group(1))

      gpsTimeMatch = re.search(self.GPSTIME, line)
      if gpsTimeMatch == None:
        gpsTime.append('None:')
      else:
        gpsTime.append(gpsTimeMatch.group(1))

    # adding all lists of fields to the raw dictionary
    self.rawDict = {
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

    #  adding only selected lists of fields to the stript dictionary
    self.striptDict = {
      'System Time': systemTime,
      'Zooloo Time': zooloo,
      'Date': date,
      'IMSI': imsi,
      'IMEI': imei,
      'TMSI': tmsi,
      'LAT': lat,
      'LONG': long,
      'COURSE': course,
      'TAC': tac,
      'TA': ta,
      'GPS Date': gpsDate,
      'GPS Time': gpsTime
      }


  def DisplayRawDataFields(self):

    for rexLists in self.rawDict.values():
      for match in rexLists:
        print(match)


  def DisplayStriptDataFields(self):

    for rexLists in self.striptDict.values():
      for match in rexLists:
        print(match)


  def VarifyDataFields(self):

    a = len(self.self.rawDict.get('System Time'))
    b = len(self.self.rawDict.get('Zooloo Time'))
    c = len(self.self.rawDict.get('Date'))
    d = len(self.self.rawDict.get('IMSI'))
    e = len(self.self.rawDict.get('IMEI'))
    f = len(self.self.rawDict.get('TMSI'))
    g = len(self.self.rawDict.get('LAT'))
    h = len(self.self.rawDict.get('LONG'))
    i = len(self.self.rawDict.get('COURSE'))
    j = len(self.self.rawDict.get('SPEED'))
    k = len(self.self.rawDict.get('ALT'))
    l = len(self.self.rawDict.get('CAUSE'))
    m = len(self.self.rawDict.get('TAC'))
    n = len(self.self.rawDict.get('TA'))
    o = len(self.self.rawDict.get('GPS Date'))
    p = len(self.self.rawDict.get('GPS Time'))

    checklist = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]
    baseline = max(checklist)
    count = 0
    for datapoint in checklist:
      if datapoint != baseline:
        print('Data item at index: ',count, ': has the value of: ', datapoint, 'and the target is: ',baseline)
        break
      count +=1


  def WriteRawFiles(self):

    p = ''
    today = datetime.datetime.today()
    filename = ('rawData - {:%b-%d,%Y-%H-%M}.json'.format(today))
    pathToFile = p.join(('rawFiles/',filename))
    with open(pathToFile, 'w') as f:
      json.dump(self.rawDict, f)

    print("Raw Data Written!")


  def WriteStriptFiles(self):

    p = ''
    today = datetime.datetime.today()
    filename = ('striptData - {:%b-%d,%Y-%H-%M}.json'.format(today))
    pathToFile = p.join(('striptFiles/',filename))
    with open(pathToFile, 'w') as f:
      json.dump(self.striptDict, f)

    print("Stript Data Written!")


  def ReformatData(self):
    pass


if __name__ == '__main__':
  print("Starting")
  # initializing a RockerParse instance
  rkr = RockerParse()

  # accessing the file paths
  inFile = rkr.path

# Reads the log file and returns each line
  line = rkr.ReadFile(inFile)

  # builds up the dictionaries based on RegEx
  rkr.BuildRegExDictionaries(line)

  # Displays the data in the raw data dictionary
  # rkr.DisplayRawDataFields()

  # Displays the data in the stript dictionary
  rkr.DisplayStriptDataFields()

  # verifies that all datafields are present
  # rkr.VarifyDataFields()

  # Writes raw data to json file
  # rkr.WriteRawFiles()

  # Writes all stript data to json file
  # rkr.WriteStriptFiles()
