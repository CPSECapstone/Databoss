import models

# Sets up the tables in the database and their connections. Should be called only once.
def createTable():
    models.db.create_all()
    models.db.session.commit()

# Add capture to capture table with references to associated files
def addCapture(name, startTime, endTime, dbId, logfileId, metricId):
    new_cap = models.Capture(name, startTime, endTime, dbId, logfileId, metricId)
    models.db.session.add(new_cap)
    models.db.session.commit()

# Return all captures in the capture table
def getCaptureAll():
    cap_list = models.Capture.query.with_entities(models.Capture.id, models.Capture.name, models.Capture.startTime)
    return cap_list

# Add replay to replay table with references to associated files
def addReplay(name, startTime, endTime, dbId, logfileId, metricId, captureId):
    new_rep = models.Replay(name, startTime, endTime, dbId, logfileId, metricId, captureId)
    models.db.session.add(new_rep)
    models.db.session.commit()

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
def getMetric(metricId):
    m = models.Metric.query.get(metricId)
    return m

# Add logfile to the logfile table
def addLogfile(name, bucket, file):
    new_logfile = models.Logfile(name, bucket, file)
    models.db.session.add(new_logfile)
    models.db.session.commit()

# Return logfile associated with provided capture or replay
def getLogfile(logfileId):
    log = models.Logfile.query.get(logfileId)
    return log
