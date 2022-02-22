#!/usr/bin/python3

import re
import sys
import io
import os
import fnmatch
import datetime
import time
import csv
import zulu
import geohash


class RockerParse:

  def __init__(self):
    self.lines = []
    self.rawDataList = []
    self.striptDataList = []

    # defining the regular expressions for each field
    self.SYSTEMTIME = re.compile(r'(?P<SystemTimeValue>^\d{2}:\d{2}:\d{2})\s?')
    self.ZULU = re.compile(r'\[(?P<ZuluTnimeValue>\d{2}:\d{2}:\d{2})\]')
    self.DATE = re.compile(r'\[(?P<DateValue>\d{8})\]')
    self.IMSI = re.compile(r'IMSI:(?P<IMSIValue>[0-9]+):')
    self.IMEI = re.compile(r'IMEI:(?P<IMEIValue>[0-9]+):')
    self.TMSI = re.compile(r'TMSI:(?P<TMSIValue>0xF+):')
    self.LAT = re.compile(r'LAT:(?P<direction>[NS])(?P<LatValue>[0-9]+\.[0-9]+):')
    self.LONG = re.compile(r'LONG:(?P<direction>[EW])(?P<LongValue>[0-9]+\.[0-9]+):')
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
        path = p.join(("./convertedLogs/", file))

    try:
      with open(path, 'r') as fin:
        self.lines = fin.readlines()

    except FileNotFoundError:
      print("File not found!")


  def BuildRegExDictionaries(self):

    for line in self.lines:
      rawDict = {}
      striptDict = {}

    # add all matches to a list
      systemTimeMatch = re.search(self.SYSTEMTIME, line)
      # if systemTimeMatch == None:
        # rawDict['System Time'] = 'None:'
        # striptDict['System Time'] = 'None:'
      # else:
        # rawDict['System Time'] = systemTimeMatch.group(1)
        # striptDict['System Time'] = systemTimeMatch.group(1)

      zuluTimeMatch = re.search(self.ZULU, line)
      # if zuluTimeMatch == None:
        # rawDict['Zulu'] = 'None:'
        # striptDict['Zulu'] = 'None:'
      # else:
        # rawDict['Zulu'] = zuluTimeMatch.group(1)
        # striptDict['Zulu'] = zuluTimeMatch.group(1)

      dateMatch = re.search(self.DATE, line)
      # if dateMatch == None:
        # rawDict['Date'] = 'None:'
        # striptDict['Date'] = 'None:'
      # else:
        # rawDict['Date'] = dateMatch.group(1)
        # striptDict['Date'] = dateMatch.group(1)

      ts = ''
      zTime = ts.join((dateMatch.group(1),' ',zuluTimeMatch.group(1)))
      zuluFormat = zulu.parse(zTime)
      zuluFormat.timestamp()
      rawDict['Timestamp'] = zuluFormat
      striptDict['Timestamp'] = zuluFormat

      imsiMatch = re.search(self.IMSI, line)
      if imsiMatch == None:
        rawDict['IMSI'] = 'None:'
        striptDict['IMSI'] = 'None:'
        # self.rawDataList.append(rawDict)
        # self.striptDataList.append(striptDict)
      else:
        rawDict['IMSI'] = imsiMatch.group(1)
        striptDict['IMSI'] = imsiMatch.group(1)
        # self.rawDataList.append(rawDict)
        # self.striptDataList.append(striptDict)

      imeiMatch = re.search(self.IMEI, line)
      if imeiMatch == None:
        rawDict['IMEI'] = 'None:'
        striptDict['IMEI'] = 'None:'
        # self.rawDataList.append(rawDict)
        # self.striptDataList.append(striptDict)
      else:
        rawDict['IMEI'] = imeiMatch.group(1)
        striptDict['IMEI'] = imeiMatch.group(1)
        # self.rawDataList.append(rawDict)
        # self.striptDataList.append(striptDict)

      tmsiMatch = re.search(self.TMSI, line)
      if tmsiMatch == None:
        rawDict['TMSI'] = 'None:'
        # self.rawDataList.append(rawDict)
      else:
        rawDict['TMSI'] = tmsiMatch.group(1)
        # self.rawDataList.append(rawDict)

      latMatch = re.search(self.LAT, line)
      if latMatch == None:
        rawDict['Latitude'] = 'None:'
        striptDict['Latitude'] = 'None:'
      else:
        direction = latMatch.group(1)
        lat = latMatch.group(2)
        latitude = ''
        if direction == 'S':
          latitude = ''.join(('-', str(lat)))
          rawDict['Latitude'] = latitude
          striptDict['Latitude'] = latitude
        else:
          rawDict['Latitude'] = lat
          striptDict['Latitude'] = lat

      longMatch = re.search(self.LONG, line)
      if longMatch == None:
        rawDict['Longitude'] = 'None:'
        striptDict['Longitude'] = 'None:'
      else:
        direction = longMatch.group(1)
        long = longMatch.group(2)
        longitude = ''
        if direction == 'W':
          longitude = ''.join(('-', str(long)))
          rawDict['Longitude'] = longitude
          striptDict['Longitude'] = longitude
        else:
          rawDict['Longitude'] = long
          striptDict['Longitude'] = long

      courseMatch = re.search(self.COURSE, line)
      if courseMatch == None:
        rawDict['Course'] = 'None:'
        # self.rawDataList.append(rawDict)
      else:
        rawDict['Course'] = courseMatch.group(1)
        # self.rawDataList.append(rawDict)

      speedMatch = re.search(self.SPEED, line)
      if speedMatch == None:
        rawDict['Speed'] = 'None:'
        # self.rawDataList.append(rawDict)
      else:
        rawDict['Speed'] = speedMatch.group(1)
        # self.rawDataList.append(rawDict)

      altMatch = re.search(self.ALT, line)
      if altMatch == None:
        rawDict['Alt'] = 'None:'
        # self.rawDataList.append(rawDict)
      else:
        rawDict['Alt'] = altMatch.group(1)
        # self.rawDataList.append(rawDict)

      causeMatch = re.search(self.CAUSE, line)
      if causeMatch == None:
        rawDict['Cause'] = 'None:'
        # self.rawDataList.append(rawDict)
      else:
        rawDict['Cause'] = causeMatch.group(1)
        # self.rawDataList.append(rawDict)

      tacMatch = re.search(self.TAC, line)
      if tacMatch == None:
        rawDict['Tac'] = 'None:'
        # self.rawDataList.append(rawDict)
      else:
        rawDict['Tac'] = tacMatch.group(1)
        # self.rawDataList.append(rawDict)

      taMatch = re.search(self.TA, line)
      if taMatch == None:
        rawDict['Ta'] = 'None:'
        # self.rawDataList.append(rawDict)
      else:
        rawDict['Ta'] = taMatch.group(1)
        # self.rawDataList.append(rawDict)

      gpsDateMatch = re.search(self.GPSDATE, line)
      if gpsDateMatch == None:
        rawDict['GPS Date'] = 'None:'
        # self.rawDataList.append(rawDict)
      else:
        rawDict['GPS Date'] = gpsDateMatch.group(1)
        # self.rawDataList.append(rawDict)

      gpsTimeMatch = re.search(self.GPSTIME, line)
      if gpsTimeMatch == None:
        rawDict['GPS Time'] = 'None:'
        # self.rawDataList.append(rawDict)
      else:
        rawDict['GPS Time'] = gpsTimeMatch.group(1)
        # self.rawDataList.append(rawDict)

    # Adding dictionaries to list
      self.rawDataList.append(rawDict)
      self.striptDataList.append(striptDict)


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
    b = len(self.self.rawDict.get('Zulu'))
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
    columnHeaders = ['Timestamp', 'IMSI', 'IMEI', 'TMSI', 'Latitude', 'Longitude', 'Course', 'Speed', 'Alt', 'Cause', 'Tac', 'Ta', 'GPS Date', 'GPS Time']

    p = ''
    today = datetime.datetime.today()
    filename = ('rawData - {:%b-%d,%Y-%H-%M}.csv'.format(today))
    pathToFile = p.join(('rawFiles/',filename))
    with open(pathToFile, 'w') as f:
      writer = csv.DictWriter(f, fieldnames=columnHeaders)
      writer.writeheader()

      for data in self.rawDataList:
          writer.writerow(data)

    print("Raw Data Written!")


  def WriteStriptFiles(self):
    columnHeaders = ['Timestamp', 'IMSI', 'IMEI', 'Latitude', 'Longitude']

    p = ''
    today = datetime.datetime.today()
    filename = ('striptData - {:%b-%d,%Y-%H-%M}.csv'.format(today))
    pathToFile = p.join(('striptFiles/',filename))
    with open(pathToFile, 'w') as f:
      writer = csv.DictWriter(f, fieldnames=columnHeaders)
      writer.writeheader()

      for data in self.striptDataList:
          writer.writerow(data)

    print("Stript Data Written!")


if __name__ == '__main__':
  print("Starting")
  # initializing a RockerParse instance
  rkr = RockerParse()

  # builds up the dictionaries based on RegEx
  rkr.BuildRegExDictionaries()

  # Displays the data in the dictionaries
  # rkr.DisplayRawDataFields()
  # rkr.DisplayStriptDataFields()

  # verifies that all datafields are present
  # rkr.VarifyDataFields()

  # Writes data to csv file
  rkr.WriteRawFiles()
  rkr.WriteStriptFiles()
