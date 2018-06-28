import re
from elasticsearch import Elasticsearch

# path of log file
infile = r"C:\Users\wangw\elk\project\2018.06.22-24_Default.0\example1.log"
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def searchEvent(filePath,es):
    with open(filePath) as f:
        f = f.readlines()
    for line in f:
        # print(line)
        list = line.split(' ')
        ev = {}
        ev["time"] = '%s %s' % (list[0],list[1])
        ev["processName"] = list[4]            
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
            ev["currentMem"] = memSet.group(1)
            ev["peakMem"] = memSet.group(2)
        print(ev)
        es.index(index='poker-dod', doc_type='document', body=ev)
        # eventList = {}
        # eventList.append('%s:%s %s' % ("time",list[0],list[1]))
        # eventList.append('%s:%s' % ("proName",list[4]))
        # print(eventList)          
    # return eventList

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

