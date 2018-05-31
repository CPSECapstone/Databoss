from threading import Timer
from datetime import timedelta
from datetime import datetime
import capture
import modelsQuery
import logging

import time
import pytz

logger = logging.getLogger()
logger.setLevel(logging.INFO)

STORAGE_CONVERSION = (10**6)

storageResult = False
t = None

def scheduleStorageCapture(startTime, storageLimit, freeSpace, captureName):
    global t
    captureObj = modelsQuery.getCaptureByName(captureName)

    if (storageResult == False):
        t = Timer(5, pollStorage, args=[startTime, storageLimit, freeSpace, captureName, captureObj])
        t.start()

def pollStorage(startTime, userStorageInput, maxSpace, captureName, captureObj):
    global storageResult

    storageMetrics = capture.cloudwatch.get_metric_statistics(Namespace='AWS/RDS',
                                     MetricName='FreeStorageSpace',
                                     StartTime=datetime.now() - timedelta(minutes=1),
                                     EndTime=datetime.now(),
                                     Period=60,
                                     Statistics=['Average']
                                     )
    #print("storage metrics: ")
    #print(storageMetrics)
    for element in storageMetrics['Datapoints'][0:]:
        mbVal = (element['Average'])/(STORAGE_CONVERSION)
        #print("mbVal: ", mbVal)
        #print(maxSpace - mbVal)
        if ((maxSpace - mbVal) >= userStorageInput):
            storageResult = True
            endCapture(captureObj, startTime, datetime.now())

    if (storageResult == False):
        time.sleep(5)
        captureObj = modelsQuery.getCaptureByName(captureName)
        pollStorage(startTime, userStorageInput, maxSpace, captureName, captureObj)


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
    rdsInstance = captureObj.dbName
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

    rdsInstance = captureObj.dbName
    database = None

    startTime = datetime.strftime(startTime.replace(tzinfo=pytz.utc), '%a, %d %b %Y %H:%M:%S %Z')

    capture.stopCapture('time', rdsInstance, database, startTime, endTime, captureObj.name, captureObj.logfileId,
                        captureObj.metricId, captureFileName, metricFileName)
