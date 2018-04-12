import models
import modelsQuery
import sqlite3
from web_app import db

import datetime

# Currently functions only on the main DB, and the main DB have tables created and empty

backupDB = sqlite3.connect(':memory:')
mainDB = sqlite3.connect('database.db')

def testSetup():
    query = "".join(line for line in mainDB.iterdump())
    backupDB.executescript(query)
    db.drop_all()
    db.create_all()

def testAddGetMetric():
    name = 'metName'
    bucket = 'metBucket'
    filename = 'metFile'
    modelsQuery.addMetric(name, bucket, filename)
    result = models.Metric.query.filter_by(name=name, bucket=bucket, filename=filename).count()
    assert result == 1

    metric = modelsQuery.getMetricById(1)
    assert metric.name == name
    assert metric.bucket == bucket
    assert metric.filename == filename

def testAddGetLogfile():
    id = 1
    name = 'logName'
    bucket = 'logBucket'
    filename = 'logFile'
    modelsQuery.addLogfile(name, bucket, filename)
    result = models.Logfile.query.filter_by(id=id).count()
    assert result == 1

    log = modelsQuery.getLogfile(id)
    assert log.id == id
    assert log.name == name
    assert log.bucket == bucket
    assert log.filename == filename

def testAddCapture():
    name = 'capName'
    startTime = datetime.datetime(2018, 1, 31, 10, 10, 10)
    endTime = datetime.datetime(2018, 1, 31, 11, 11, 11)
    dbName = 'myrds'
    logfileId = 1
    metricId = 1
    mode = "interactive"
    status = "active"
    modelsQuery.addCapture(name, startTime, endTime, dbName, logfileId, metricId, mode, status)
    result = models.Capture.query.get(1)
    assert result.name == name
    assert result.startTime == startTime
    assert result.endTime == endTime
    assert result.dbName == dbName
    assert result.logfileId == logfileId
    assert result.metricId == metricId
    assert result.mode == mode
    assert result.status == status

def testGetCapture():
    list = modelsQuery.getCaptureAll().count()
    assert list == 1
    name = 'capName2'
    dbName = 'myrds'
    startTime = datetime.datetime(2018, 1, 31, 12, 12, 12)
    endTime = datetime.datetime(2018, 1, 31, 12, 13, 13)
    logfileId = 1
    metricId = 1
    mode = "interactive"
    status = "active"
    modelsQuery.addCapture(name, startTime, endTime, dbName, logfileId, metricId, mode, status)
    list = modelsQuery.getCaptureAll().count()
    assert list == 2

def testAddReplay():
    name = 'repName'
    startTime = datetime.datetime(2018, 1, 31, 10, 10, 10)
    endTime = datetime.datetime(2018, 1, 31, 11, 11, 11)
    dbName = "myrds"
    metricId = 1
    captureId = 1
    mode = "replay-raw"
    status = "active"
    modelsQuery.addReplay(name, startTime, endTime, dbName, metricId, captureId, mode, status)
    result = models.Replay.query.get(1)
    assert result.name == name
    assert result.startTime == startTime
    assert result.endTime == endTime
    assert result.dbName == dbName
    assert result.metricId == metricId
    assert result.captureId == captureId
    assert result.mode == mode
    assert result.status == status

def testGetReplay():
    list = modelsQuery.getReplayAll().count()
    assert list == 1

    name = 'repName2'
    startTime = datetime.datetime(2018, 1, 31, 12, 12, 12)
    endTime = datetime.datetime(2018, 1, 31, 12, 13, 13)
    dbName = "rds2"
    metricId = 2
    captureId = 2
    mode = "replay-raw"
    status = "active"
    modelsQuery.addReplay(name, startTime, endTime, dbName, metricId, captureId, mode, status)
    list = modelsQuery.getReplayAll().count()
    assert list == 2

def testGetAllCaptures():
    # make sure there are already two captures in the list
    list = modelsQuery.getCaptureAll().count()

    assert list == 2
    # Adding first capture
    modelsQuery.addCapture(
        'capture1',
        datetime.datetime(2018, 1, 1, 10, 10, 10),
        datetime.datetime(2018, 1, 1, 11, 11, 11),
        'myrds',
        1,
        1,
        "interactive",
        "active"
    )
    #Adding second capture
    modelsQuery.addCapture(
        'capture2',
        datetime.datetime(2018, 2, 2, 10, 10, 10),
        datetime.datetime(2018, 2, 2, 11, 11, 11),
        'myrds',
        1,
        1,
        "interactive",
        "active"
    )
    list = modelsQuery.getCaptureAll().count()
    assert list == 4



def testCleanup():
    db.drop_all()
    db.create_all()

    for line in backupDB.iterdump():
        if 'Capture' in line:
            query = line
            mainDB.executescript(query)
        if 'Replay' in line:
            query = line
            mainDB.executescript(query)
        if 'Metric' in line:
            query = line
            mainDB.executescript(query)
        if 'Logfile' in line:
            query = line
            mainDB.executescript(query)
        if 'DBConnection' in line:
            query = line
            mainDB.executescript(query)
    backupDB.close()
    mainDB.close()
