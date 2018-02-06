import models
import modelsQuery

import datetime


def testAddGetMetric():
    name = 'metName'
    bucket = 'metBucket'
    file = 'metFile'
    modelsQuery.addMetric(name, bucket, file)
    result = models.Metric.query.filter_by(name=name, bucket=bucket, file=file).count()
    assert result == 1

def testAddGetLogfile():
    name = 'logName'
    bucket = 'logBucket'
    file = 'logFile'
    modelsQuery.addLogfile(name, bucket, file)
    result = models.Logfile.query.filter_by(name=name, bucket=bucket, file=file).count()
    assert result == 1

def testAddCapture():
    name = 'capName'
    startTime = datetime.datetime(2018, 1, 31, 10, 10, 10)
    endTime = datetime.datetime(2018, 1, 31, 11, 11, 11)
    dbId = 1
    logfileId = 1
    metricId = 1
    modelsQuery.addCapture(name, startTime, endTime, dbId, logfileId, metricId)
    result = models.Capture.query.filter_by(name=name, startTime=startTime, endTime=endTime).count()
    assert result == 1

def testGetCapture():
    list = modelsQuery.getCaptureAll().count()
    assert list == 1

def testAddReplay():
    name = 'repName'
    startTime = datetime.datetime(2018, 1, 31, 10, 10, 10)
    endTime = datetime.datetime(2018, 1, 31, 11, 11, 11)
    dbId = 1
    logfileId = 1
    metricId = 1
    captureId = 1
    modelsQuery.addReplay(name, startTime, endTime, dbId, logfileId, metricId, captureId)
    result = models.Replay.query.filter_by(name=name, startTime=startTime, endTime=endTime, captureId=captureId).count()
    assert result == 1

def testGetReplay():
    list = modelsQuery.getReplayAll().count()
    assert list == 1
