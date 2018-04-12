from threading import Timer
from datetime import timedelta
from datetime import datetime
import capture
import modelsQuery
import logging
import pytz


logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
