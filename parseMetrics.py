import json


cpuList = []
cpuTimeList = []
readIOList = []
readIOTimeList = []
writeIOList = []
writeIOTimeList = []

def readMetricsFile(textFile):
    tempList = []
    f = open(textFile, "r")
    tempData = json.loads(f.read())
    createCPULists(tempData)

    #createCPULists(f)
    #f.close();
    #tempData[\"Label:" "CPUUtilization", "Datapoints"]

def createCPULists(openFile):
    #cpuList = []
    #cpuTimeList = []
    cpuData = openFile[0]
    for element in cpuData['Datapoints']:
        cpuTimeList.append(element['Timestamp'])
        cpuList.append(element['Average'])




#array = '{"drinks": ["coffee", "tea", "water"]}'
#data = json.loads(array)

#for element in data['drinks']:
#    print(element)




readMetricsFile("metric-file.txt")

