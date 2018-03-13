from threading import Timer
from datetime import timedelta
from datetime import datetime
import capture
import modelsQuery
import logging
import sys
import pytz

logger = logging.getLogger()
logger.setLevel(logging.INFO)

storageResult = False

def scheduleStorageCapture(startTime, storageLimit, allocatedStorage, captureName):
    captureObj = modelsQuery.getCaptureByName(captureName)

    t = Timer(0, pollStorage, args=[startTime, storageLimit, allocatedStorage, captureObj])
    t.start()
    while (storageResult == False):
        t = Timer(60, pollStorage, args=[startTime, storageLimit, allocatedStorage, captureObj])
        t.start()

def pollStorage(startTime, userStorageInput, maxUserStorage, captureObj):
    global storageResult

    storageMetrics = capture.cloudwatch.get_metric_statistics(Namespace='AWS/RDS',
                                     MetricName='FreeStorageSpace',
                                     StartTime=datetime.utcnow() - timedelta(minutes=1),
                                     EndTime=datetime.utcnow(),
                                     Period=60,
                                     Statistics=['Average']
                                     )
    print("storage metrics: ")
    print(storageMetrics)
    freeSpace = (storageMetrics['Datapoints'][0]['Average']) /(10**6)
    for element in storageMetrics['Datapoints'][0:]:
        mbVal = (element['Average'])/(10**6)
        if (freeSpace - mbVal) == userStorageInput:
            storageResult = True
            endCapture(captureObj, startTime, datetime.now())
    storageResult = False

def scheduleCapture(captureName):
    captureObj = modelsQuery.getCaptureByName(captureName)
    startTime = captureObj.startTime
    endTime = captureObj.endTime

    whenToStart = (startTime - datetime.now()).seconds
    whenToEnd = (endTime - datetime.now()).total_seconds()

    t1 = Timer(whenToStart, startCapture, args={captureObj})
    t2 = Timer(whenToEnd, endCapture, [captureObj, startTime, endTime])
    t1.start()
    t2.start()

def startCapture(captureObj):
    rdsInstance = captureObj.dbName.split("/")[0]
    status_of_db = capture.get_list_of_instances(rdsInstance)['DBInstances'][0]['DBInstanceStatus']

    if status_of_db != "available":
        capture.rds.start_db_instance(
            DBInstanceIdentifier=rdsInstance
        )

    modelsQuery.updateCaptureStatus(captureObj.name, "active")

def endCapture(captureObj, startTime, endTime):
    captureFileName = captureObj.name + " " + "capture file"
    metricFileName = captureObj.name + " " + "metric file"
    modelsQuery.updateCaptureStatus(captureObj.name, "finished")

    rdsInstance, database = captureObj.dbName.split("/")

    startTime = datetime.strftime(startTime.replace(tzinfo=pytz.utc), '%a, %d %b %Y %H:%M:%S %Z')

    capture.stopCapture(rdsInstance, database, startTime, endTime, captureObj.name, captureObj.logfileId,
                        captureObj.metricId, captureFileName, metricFileName)
