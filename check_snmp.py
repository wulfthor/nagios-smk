#! /usr/bin/python

import sys
import os
import numpy


status = { 'OK' : 0 , 'WARNING' : 1, 'CRITICAL' : 2 , 'UNKNOWN' : 3}


host =  sys.argv[1]
warn_value = int(sys.argv[2])
#warn_value = 80
crit_value = int(sys.argv[3])
#crit_value = 85
# An array with the partitions we are not interested in.
blacklist =  ['Memory_Buffer', 'Swap_Space', 'Real_Memory', 'contract'  , 'proc', 'dev', 'run', 'mnttab' , 'svc', 'zones', 'nfs', 'object', 'system', 'vol', 'platform', 'export' , 'sys', 'Swap', 'Physical', 'Virtual', 'boot']


desc_ =  os.popen('/usr/bin/snmpwalk -v 2c -Os -c public ' + host + ' hrStorageDescr').readlines()
size_ =  os.popen('/usr/bin/snmpwalk -v 2c -Os -c public ' + host + ' hrStorageSize').readlines()
used_ =  os.popen('/usr/bin/snmpwalk -v 2c -Os -c public ' + host + ' hrStorageUsed').readlines()

# not in order, so use a dictinary
desc = dict()
size = dict()
used = dict()
for line in size_:
  print line

for line in desc_:
  print line
  desc [ line.split()[0].replace('hrStorageDescr.', '') ] =  line.split()[3]

for key in desc.keys() :
  for line in size_ :
    if 'hrStorageSize.' + key in line:
      size [ key ] =  line.split()[3]
      for line in used_ :
        if 'hrStorageUsed.' + key in line:
          used [ key ] =  line.split()[3]


numpy.seterr(divide = 'ignore')


for key in used.keys():
  try :
    used[key] = long(used[key]) * 100 / long(size[key])
  except ZeroDivisionError:
    used[key] = 0


data = ''
warn=False
crit=False
d = dict()

def blacklisted(key):
  for word in blacklist:
    if word in key:
      return True
    return False

for key in used.keys():
  if not blacklisted(desc[key]) :
    data +=   desc[key] +  '  ' +   str(used[key] )  + '%, '
    if used[key] >= warn_value :
      warn=True
      if used[key] >= crit_value :
        crit=True

if warn == True:

       if crit == True:
         print 'DISK: ' + data.strip()
         sys.exit(status['CRITICAL'])
       else:
         print 'DISK: ' + data.strip()
         sys.exit(status['WARNING'])

else:
  print 'DISK: '  + data.strip()
  sys.exit(status['OK'])

def main():

        count=20
        method="searcht"
        origstring=""
        optionstr=""
        filelocation="/tmp/test.txt"
        test=0
        debug=0
        lang="da"

        try:
          opts, args = getopt.getopt(sys.argv[1:],"s:g:h:m:c:dta:f:i:j:w:")
          for o, a in opts:
            if o == "-s":
              origstring = a
              searchstring = urllib2.quote(a.encode('utf8'))
            elif o == "-g":
              fromdate = a
              optionstr=optionstr+"&from-date="+fromdate
            elif o == "-h":
              todate = a
              optionstr=optionstr+"&to-date="+todate
            elif o == "-i":
              tag = a
              optionstr=optionstr+"&tag=type/"+tag
            elif o == "-m":
              method = a
            elif o == "-c":
              count = a
              optionstr=optionstr+"&page-size="+count
            elif o == "-j":
              pagenumber = a
              optionstr=optionstr+"&page="+pagenumber
            elif o == "-w":
              wordcount = a
              optionstr=optionstr+"&min-wordcount=2&max-wordcount="+wordcount
            elif o == "-t":
              test = 1
            elif o == "-d":
              debug = 1
            elif o == "-f":
              filelocation = a
            elif o == "-l":
              lang = a
            else:
              assert False, "unhandled option"

        except getopt.GetoptError as err:
          print(err)
          sys.exit(2)

