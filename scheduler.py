from threading import Timer
from datetime import timedelta
from datetime import datetime
import capture
import modelsQuery

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

