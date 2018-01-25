import json

cpuList = []
cpuTimeList = []
readIOList = []
readIOTimeList = []
writeIOList = []
writeIOTimeList = []
memoryList = []
memoryTimeList = []


def readMetricsFile(textFile):
    tempList = []
    f = open(textFile, "r")
    tempData = json.loads(f.read())
    return tempData

def createLists(dictData, timeArray, dataArray):
    timeArray.clear()
    dataArray.clear()
    for element in dictData['Datapoints']:
        timeArray.append(element['Timestamp'])
        dataArray.append(element['Average'])

def createCPULists(openFile):
    cpuData = openFile[0]
    createLists(cpuData, cpuTimeList, cpuList)
    _sortLists(cpuList, cpuTimeList)


def createReadIOLists(openFile):
    readIOData = openFile[1]
    createLists(readIOData, readIOTimeList, readIOList)


def createWriteIOLists(openFile):
    writeIOData = openFile[2]
    createLists(writeIOData, writeIOTimeList, writeIOList)


def createMemLists(openFile):
    memData = openFile[3]
    createLists(memData, memoryTimeList, memoryList)


def _sortLists(dataList, timeList):
    zipped = zip(timeList, dataList)
    times, metrics = map(list, zip(*sorted(zipped, key=lambda data: data[0])))
    dataList.clear()
    timeList.clear()

    for metric in metrics:
        dataList.append(metric)

    for time in times:
        timeList.append(time)


# openFile = readMetricsFile("metric_files/metric-file.txt")
# createCPULists(openFile)
# createReadIOLists(openFile)
# createWriteIOLists(openFile)
#
