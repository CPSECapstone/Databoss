import json

class ParsedMetrics:
    def __init__(self, jsonString):
        self.jsonString = jsonString
        self.cpuList = []
        self.cpuTimeList = []
        self.readIOList = []
        self.readIOTimeList = []
        self.writeIOList = []
        self.writeIOTimeList = []
        self.memoryList = []
        self.memoryTimeList = []

        jsonMetrics = readMetrics(self.jsonString)
        createLists(jsonMetrics[0], self.cpuTimeList, self.cpuList)
        createLists(jsonMetrics[1], self.readIOTimeList, self.readIOList)
        createLists(jsonMetrics[2], self.writeIOTimeList, self.writeIOList)
        createLists(jsonMetrics[3], self.memoryTimeList, self.memoryList)

# Convert a json string to an array of json objects
def readMetrics(jsonString):
    tempData = json.loads(jsonString)
    return tempData

# Populate data and time list given a dict with elements having a timestamp and average key
def createLists(dictData, timeArray, dataArray):
    for element in dictData['Datapoints']:
        timeArray.append(element['Timestamp'])
        dataArray.append(element['Average'])

    _sortLists(dataArray, timeArray)

# Sort data list and time list together to preserve correct data ordering, in ascending time order
def _sortLists(dataList, timeList):
    if len(dataList) > 0:
        # Combine, sort and separate the two lists
        zipped = zip(timeList, dataList)
        times, metrics = map(list, zip(*sorted(zipped, key=lambda data: data[0])))

        dataList.clear()
        timeList.clear()

        for metric in metrics:
            dataList.append(metric)

        for time in times:
            timeList.append(time)