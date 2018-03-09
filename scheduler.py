from threading import Timer
from datetime import timedelta
from datetime import datetime
import capture
import modelsQuery
import logging
import sys


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def pollStorage(userStorageInput, maxUserStorage):

        t = Timer(datetime.now(), capture.checkStorageCapacity(userStorageInput, maxUserStorage))
        t.start()

def parseJson(jsonString, storage_limit):
    freeSpace = (jsonString['Datapoints'][0]['Average'])/(10 **9)
    if (storage_limit > freeSpace):
        logger.error("ERROR: Not enough space for this.")
        sys.exit()
    else:
        storageRem = freeSpace - storage_limit
        for element in jsonString['Datapoints'][1:]:
            gbVal = (element['Average'])/(10 ** 9)
            #if (gbVal <= storageRem):   #Storage limit has been met
                #CALL stopCapture()

#storage_limit should be in gb
def checkStorageCapacity(storage_limit, storage_max_db):
    db_name = rds_config.db_name
    if (storage_limit > storage_max_db):
        print("ERROR: Storage specified is greater than what", db_name, "has allocated")
        sys.exit()
    else:
        parseJson(cloudwatch.get_metric_statistics(Namespace = 'AWS/RDS',
                                    MetricName = 'FreeStorageSpace',
                                    StartTime=datetime.utcnow() - timedelta(minutes=60),
                                    EndTime=datetime.utcnow(),
                                    Period= 300,
                                    Statistics=['Average']
                                        ), storage_limit)

def scheduleCapture(captureName):
    captureObj = modelsQuery.getCaptureByName(captureName)
    startTime = captureObj.startTime
    endTime = captureObj.endTime

    timeDiff = endTime - startTime
    if timeDiff.total_seconds() > 86400:
        endTime = startTime + timedelta(minutes=1440)

    whenToStart = (startTime - datetime.now()).seconds
    whenToEnd = (endTime - startTime).total_seconds()

    t1 = Timer(whenToStart, startCapture, args={captureObj})
    t2 = Timer(whenToEnd, endCapture, [captureObj, startTime, endTime])
    t1.start()
    t2.start()

def startCapture(captureObj):
    dbName = captureObj.dbName
    status_of_db = capture.get_list_of_instances(dbName)['DBInstances'][0]['DBInstanceStatus']

    if status_of_db != "available":
        capture.rds.start_db_instance(
            DBInstanceIdentifier=dbName
        )

    modelsQuery.updateCaptureStatus(captureObj.name, "active")

def endCapture(captureObj, startTime, endTime):
    print("object")
    print(captureObj)
    captureFileName = captureObj.name + " " + "capture file"
    metricFileName = captureObj.name + " " + "metric file"
    modelsQuery.updateCaptureStatus(captureObj.name, "finished")

    print("stop capture")
    capture.stopCapture(startTime, endTime, captureObj.name, captureObj.logfileId, captureObj.metricId, captureFileName, metricFileName)

