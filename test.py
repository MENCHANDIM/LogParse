import re
from elasticsearch import Elasticsearch
import datetime
import os

# path of log file
infile = r"C:\Users\wangw\elk\project\2018.06.22-24_Default.0\example1.log"
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def searchEvent(filePath,es):
    if os.path.exists(filePath):
        with open(filePath) as f:
            try:
                timeNow = datetime.datetime.now().isoformat().lower()
                print(timeNow)
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
                    
                    # regex for matching current memory and peak memory
                    memSet = re.match(r'.*MEM\[(\d*):(\d*)\].*', line)
                    if memSet:
                        ev["currentMem"] = int(memSet.group(1))
                        ev["peakMem"] = int(memSet.group(2))
                    ev["description"] = line.split('  ',1)[1]
                    print(ev)
                    es.index(index=timeNow, doc_type='document', body=ev)
            except:
                print("Problems occur while opening the file.")
    else:
        print("File does not exist.")

searchEvent(infile,es)

