import json

class ParsedMetrics:
    def __init__(self, file):
        self.file = file
        self.cpuList = []
        self.cpuTimeList = []
        self.readIOList = []
        self.readIOTimeList = []
        self.writeIOList = []
        self.writeIOTimeList = []
        self.memoryList = []
        self.memoryTimeList = []

        openFile = readMetricsFile(self.file)
        createLists(openFile[0], self.cpuTimeList, self.cpuList)
        createLists(openFile[1], self.readIOTimeList, self.readIOList)
        createLists(openFile[2], self.writeIOTimeList, self.writeIOList)
        createLists(openFile[3], self.memoryTimeList, self.memoryList)


def readMetricsFile(textFile):
    f = open(textFile, "r")
    tempData = json.loads(f.read())
    return tempData

def createLists(dictData, timeArray, dataArray):
    for element in dictData['Datapoints']:
        timeArray.append(element['Timestamp'])
        dataArray.append(element['Average'])

    _sortLists(dataArray, timeArray)

def _sortLists(dataList, timeList):
    if len(dataList) > 0:
        zipped = zip(timeList, dataList)
        times, metrics = map(list, zip(*sorted(zipped, key=lambda data: data[0])))
        dataList.clear()
        timeList.clear()

        for metric in metrics:
            dataList.append(metric)

        for time in times:
            timeList.append(time)