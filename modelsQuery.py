import models
from flask import jsonify

# Sets up the tables in the database and their connections. Should be called only once.
def createTable():
    models.db.create_all()
    models.db.session.commit()

def addDBConnection(dialect, name, host, port, database, username):
    exists = models.DBConnection.query.filter_by(name=name).first()
    if not exists:
        new_conn = models.DBConnection(dialect, name, host, port, database, username)
        models.db.session.add(new_conn)
        models.db.session.commit()

def getDBConnectionByName(name):
    conn = models.DBConnection.query.get(name)
    return conn

def getDBConnectionAll():
    conn_list = models.DBConnection.query.all()
    return conn_list

# Add capture to capture table with references to associated files
def addCapture(name, startTime, endTime, dbName, logfileID, metricID, mode, status):
    new_cap = models.Capture(name, startTime, endTime, dbName, logfileID, metricID, mode, status)
    models.db.session.add(new_cap)
    models.db.session.commit()

def getCaptureById(captureId):
    capture = models.Capture.query.get(captureId)
    return capture

def updateCaptureStatus(captureName, status):
    capture = models.Capture.query.filter_by(name=captureName).first()
    capture.status = status
    models.db.session.commit()

def getScheduledCaptures():
    listOfCaptures = models.Capture.query.filter_by(status="scheduled")
    return listOfCaptures

def getCaptureByName(captureName):
    capture = models.Capture.query.filter_by(name=captureName).first()
    return capture

# Return all captures in the capture table
def getCaptureAll():
    cap_list = models.Capture.query.with_entities(models.Capture.id, models.Capture.name, models.Capture.startTime)
    return cap_list

# Add replay to replay table with references to associated files
def addReplay(name, startTime, endTime, dbName, metricId, captureId, mode, status):
    new_rep = models.Replay(name, startTime, endTime, dbName, metricId, captureId, mode, status)
    models.db.session.add(new_rep)
    models.db.session.commit()

def getReplayById(replayId):
    replay = models.Replay.query.get(replayId)
    return replay

def getReplayByName(replayName):
    replay = models.Replay.query.filter_by(name=replayName).first()
    return replay

#get log file given capture name

# Return all replays in the replay table
def getReplayAll():
    rep_list = models.Replay.query.with_entities(models.Replay.id, models.Replay.name, models.Replay.startTime)
    return rep_list

# Add metric to the metric table
def addMetric(name, bucket, file):
    new_metric = models.Metric(name, bucket, file)
    models.db.session.add(new_metric)
    models.db.session.commit()

# Return metric associated with provided capture or replay
def getMetricById(metricId):
    m = models.Metric.query.get(metricId)
    return m

def getMetricByFileName(metricFileName):
    id = models.Metric.query.get(metricFileName)
    return id

def getMetricIDByNameAndBucket(metricFileName, metricBucket):
    metricObj = models.Metric.query.filter_by(name=metricFileName, bucket=metricBucket).first()
    return metricObj.id

def getMetricBucket(metricID):
    metric = models.Metric.query.filter_by(id=metricID).first()
    return metric.bucket

def getMetricFile(metricFileName, metricBucket):
    metricObj = models.Metric.query.filter_by(name=metricFileName, bucket=metricBucket).first()
    return metricObj.file

def updateMetricFile(metricID, file):
    metricObj = models.Metric.query.filter_by(id=metricID).first()
    metricObj.file = file
    models.db.session.commit()

# Add logfile to the logfile table
def addLogfile(name, bucket, file):
    new_logfile = models.Logfile(name, bucket, file)
    models.db.session.add(new_logfile)
    models.db.session.commit()

def getLogfile(logfileId):
    logObj = models.Logfile.query.filter_by(id=logfileId).first()
    return logObj

# Return logfile associated with provided capture or replay
def getLogfileById(logfileId):
    logObj = models.Logfile.query.filter_by(id=logfileId).first()
    return logObj.file

def getLogfileByName(logfileName):
    log = models.Logfile.query.filter_by(name=logfileName).first()
    return log

def getCaptureBucket(logfileID):
    log = models.Logfile.query.filter_by(id=logfileID).first()
    return log.bucket

def updateLogFile(logfileID, file):
    log = models.Logfile.query.filter_by(id=logfileID).first()
    log.file = file
    models.db.session.commit()

def getLogFile(logfileName, captureBucket):
    logObj = models.Logfile.query.filter_by(name=logfileName, bucket=captureBucket).first()
    return logObj

def getLogFileIdByNameAndBucket(logfileName, captureBucket):
    logObj = models.Logfile.query.filter_by(name=logfileName, bucket=captureBucket).first()
    return logObj.id