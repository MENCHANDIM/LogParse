infile = r"C:\Users\wangw\elk\project\2018.06.22-24_Default.0\example1.log"

def searchEvent(filePath,keyWords):
    with open(filePath) as f:
        f = f.readlines()
    eventList = []
    for line in f:
        for phrase in keyWords:
            if phrase in line:
                print(line)
                list = line.split(" ")
                eventList.append('%s %s' % (list[0],list[1]))
                break
    print(eventList)
    return eventList

local7 = searchEvent(infile,["local7"])

wpp = searchEvent(infile,["WPP"])



