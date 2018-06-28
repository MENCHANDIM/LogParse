import re
from elasticsearch import Elasticsearch
import datetime
import time

# path of log file
infile = r"C:\Users\wangw\elk\project\2018.06.22-24_Default.0\Default.0.log"
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
timeNow = datetime.datetime.now().isoformat().lower()
print(timeNow)

def searchEvent(filePath,es):
    with open(filePath) as f:
        f = f.readlines()
    for line in f:
        # print(line)
        list = line.split(' ')
        ev = {}
        logTime = '%s %s' % (list[0],list[1])
        timeArray = datetime.datetime.strptime(logTime, "%Y-%m-%d %H:%M:%S").isoformat()
        ev["logTime"] = timeArray
        ev["logLevel"] = list[2].split('.')[1]
        ev["processName"] = list[4].split(':')[0]           
        # another method to split memory data
        # if 'MEM' in line:
        # memSet = line.split('MEM')[1].split(' ')[0]
        # currentMem = memSet.split(':')[0].split('[')[1]
        # peakMem = memSet.split(':')[1].split(']')[0]
        # ev["currentMem"] = '%s' % currentMem
        # ev["peakMem"] = '%s' % peakMem
        
        # regex for matching current memory and peak memory
        memSet = re.match(r'.*MEM\[(\d*):(\d*)\].*', line)
        if memSet:
            ev["currentMem"] = int(memSet.group(1))
            ev["peakMem"] = int(memSet.group(2))
        ev["description"] = line.split('  ',1)[1]
        print(ev)
        es.index(index=timeNow, doc_type='document', body=ev)

searchEvent(infile,es)


# def searchEvent(filePath,keyWords):
#     with open(filePath) as f:
#         f = f.readlines()
#     for line in f:
#         for phrase in keyWords:
#             if phrase in line:
#                 print(line)
#                 list = line.split(" ")
#                 eventList = []
#                 eventList.append('%s:%s %s' % ("time",list[0],list[1]))
#                 eventList.append('%s:%s' % ("proName",list[4]))
#                 print(eventList)
#                 break             
#     return eventList

