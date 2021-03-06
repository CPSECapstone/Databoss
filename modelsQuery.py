import models



# Sets up the tables in the database and their connections. Should be called only once.
def createTable():
    models.db.create_all()
    models.db.session.commit()

########################
# Add queries
########################

def addDBConnection(dialect, name, host, port, database, username):
    exists = models.DBConnection.query.filter_by(name=name).first()
    if not exists:
        new_conn = models.DBConnection(dialect, name, host, port, database, username)
        models.db.session.add(new_conn)
        models.db.session.commit()

def addCapture(name, startTime, endTime, dbName, logfileID, metricID, mode, status):
    new_cap = models.Capture(name, startTime, endTime, dbName, logfileID, metricID, mode, status)
    models.db.session.add(new_cap)
    models.db.session.commit()

def addReplay(name, startTime, endTime, dbName, metricId, captureId, mode, status):
    new_rep = models.Replay(name, startTime, endTime, dbName, metricId, captureId, mode, status)
    models.db.session.add(new_rep)
    models.db.session.commit()

def addLogfile(name, bucket, file):
    new_logfile = models.Logfile(name, bucket, file)
    models.db.session.add(new_logfile)
    models.db.session.commit()

def addMetric(name, bucket, file):
    new_metric = models.Metric(name, bucket, file)
    models.db.session.add(new_metric)
    models.db.session.commit()

########################
# Delete/Remove queries
########################

def removeFinishedCapture(captureId):
    metricId = getMetricByCaptureId(captureId)
    logfileId = getLogfileByCaptureId(captureId)

    for replay in models.Replay.query.filter_by(captureId=captureId):
        removeFinishedReplay(replay.id)

    capture = models.Capture.query.filter_by(id=captureId).first()
    models.db.session.delete(capture)

    removeMetric(metricId)
    removeLogfile(logfileId)

    models.db.session.commit()

def removeFinishedReplay(replayId):
    metricId = getMetricByReplayId(replayId)
    replay = models.Replay.query.filter_by(id=replayId).first()
    models.db.session.delete(replay)
    removeMetric(metricId)
    models.db.session.commit()

def removeLogfile(logfileId):
    logfile = models.Logfile.query.filter_by(id=logfileId).first()
    models.db.session.delete(logfile)
    models.db.session.commit()

def removeMetric(metricId):
    metric = models.Metric.query.filter_by(id=metricId).first()
    models.db.session.delete(metric)
    models.db.session.commit()

########################
# Get DB queries
########################

def getDBConnectionByName(name):
    conn = models.DBConnection.query.get(name)
    return conn

def getDBConnectionAll():
    conn_list = models.DBConnection.query.all()
    return conn_list

########################
# Get Capture related queries
########################

def getCaptureById(captureId):
    capture = models.Capture.query.get(captureId)
    return capture

def getCaptureByName(captureName):
    capture = models.Capture.query.filter_by(name=captureName).first()
    return capture

# Return all captures in the capture table
def getCaptureAll():
    cap_list = models.Capture.query.with_entities(models.Capture.id, models.Capture.name, models.Capture.startTime)
    return cap_list

def getScheduledCaptures():
    listOfCaptures = models.Capture.query.filter_by(status="scheduled")
    return listOfCaptures

def getCaptureFinished():
    captures = models.Capture.query.filter_by(status="finished")
    return captures

def getCaptureActive():
    captures = models.Capture.query.filter_by(status="active")
    return captures

def getCaptureScheduled():
    captures = models.Capture.query.filter_by(status="scheduled")
    return captures

def getCaptureStartTime(captureName):
    capture = models.Capture.query.filter_by(name=captureName).first()
    return capture.startTime

def getCaptureID(captureName):
    capture = models.Capture.query.filter_by(name=captureName).first()
    if capture:
        return capture.id
    return None

def getCaptureEndTime(captureName):
    capture = models.Capture.query.filter_by(name=captureName).first()
    return capture.endTime

def getCaptureMetric(captureName):
    capture = models.Capture.query.filter_by(name=captureName).first()
    return capture.metricId

def getCaptureBucket(captureName):
    capture = models.Capture.query.filter_by(name=captureName).first()
    logObj = models.Logfile.query.filter_by(id=capture.logfileId).first()
    return logObj.bucket

def getCaptureMetricBucket(captureName):
    capture = models.Capture.query.filter_by(name=captureName).first()
    metricObj = models.Metric.query.filter_by(id=capture.metricId).first()
    return metricObj.bucket

def getCapturesWithBuckets():
    capturesWithBuckets = models.db.session.query(models.Capture, models.Logfile).filter(models.Capture.logfileId == models.Logfile.id).all();
    return capturesWithBuckets

########################
# Update Capture queries
########################

def updateCaptureStatus(captureName, status):
    capture = models.Capture.query.filter_by(name=captureName).first()
    capture.status = status
    models.db.session.commit()

def updateCaptureEndTime(captureName, endTime):
    capture = models.Capture.query.filter_by(name=captureName).first()
    capture.endTime = endTime
    models.db.session.commit()

########################
# Get Replay related queries
########################

def getReplayById(replayId):
    replay = models.Replay.query.get(replayId)
    return replay

def getReplayByName(replayName):
    replay = models.Replay.query.filter_by(name=replayName).first()
    if replay:
        return replay
    return None

# Return all replays in the replay table
def getReplayAll():
    rep_list = models.Replay.query.with_entities(models.Replay.id, models.Replay.name, models.Replay.startTime)
    return rep_list

def getReplayMetric(replayName):
    replay = models.Replay.query.filter_by(name=replayName).first()
    return replay.metricId

def getReplaysWithBuckets():
    replaysWithBuckets = models.db.session.query(models.Replay, models.Metric).filter(models.Replay.metricId == models.Metric.id).all();
    return replaysWithBuckets

########################
# Update Replay queries
########################

def updateReplayStatus(replayName, status):
    replay = models.Replay.query.filter_by(name=replayName).first()
    replay.status = status
    models.db.session.commit()

def updateReplayQueries(replayName, total, successful, failed):
    replay = models.Replay.query.filter_by(name=replayName).first()

    if replay:
        replay.totalQueries = total
        replay.successfulQueries = successful
        replay.failedQueries = failed

        models.db.session.commit()

def updateReplayEndTime(replayName, time):
    replay = models.Replay.query.filter_by(name=replayName).first()

    if replay:
        replay.endTime = time

        models.db.session.commit()

########################
# Get Metric queries
########################

# Return metric associated with provided capture or replay
def getMetricById(metricId):
    m = models.Metric.query.get(metricId)
    return m

def getMetricIDByNameAndBucket(metricFileName, metricBucket):
    metricObj = models.Metric.query.filter_by(name=metricFileName, bucket=metricBucket).first()
    return metricObj.id

def getMetricBucket(metricID):
    metric = models.Metric.query.filter_by(id=metricID).first()
    return metric.bucket

def getMetricBucketByName(name):
    capture = models.Capture.query.filter_by(name=name).first()
    metricObj = models.Metric.query.filter_by(id=capture.metricId).first()
    return metricObj.bucket

def getMetricByCaptureId(captureId):
    capture = models.Capture.query.filter_by(id=captureId).first()
    return capture.metricId

def getMetricByReplayId(replayId):
    replay = models.Replay.query.filter_by(id=replayId).first()
    return replay.metricId

########################
# Update Metric queries
########################

def updateMetricFile(metricID, filename):
    metricObj = models.Metric.query.filter_by(id=metricID).first()
    metricObj.filename = filename
    models.db.session.commit()

########################
# Get Logfile queries
########################

def getLogfile(logfileId):
    logObj = models.Logfile.query.filter_by(id=logfileId).first()
    return logObj

def getLogFileIdByNameAndBucket(logfileName, captureBucket):
    logObj = models.Logfile.query.filter_by(name=logfileName, bucket=captureBucket).first()
    return logObj.id

def getLogFileByCapture(captureName):
   captureObj = models.Capture.query.filter_by(name=captureName).first()
   logObj = models.Logfile.query.filter_by(id=captureObj.logfileId).first()
   return logObj

def getLogfileByCaptureId(captureId):
    capture = models.Capture.query.filter_by(id=captureId).first()
    return capture.logfileId

########################
# Update Metric queries
########################

# Return logfile associated with provided capture or replay
def updateLogFile(logfileID, filename):
    log = models.Logfile.query.filter_by(id=logfileID).first()
    log.filename = filename
    models.db.session.commit()
