import models


# Sets up the tables in the database and their connections. Should be called only once.
def createTable():
    models.db.create_all()
    models.db.session.commit()

# Add capture to capture table with references to associated files
def addCapture(name, time, dbId, logfileId, metricId):
    new_cap = models.Capture(name, time, dbId, logfileId, metricId)
    models.db.session.add(new_cap)
    models.db.session.commit()

# Return all captures in the capture table
def getCaptureAll():
    cap_list = models.Capture.query.with_entities(models.Capture.id, models.Capture.name, models.Capture.time)
    return cap_list

# Add replay to replay table with references to associated files
def addReplay(name, time, dbId, logfileId, metricId, captureId):
    new_rep = models.Capture(name, time, dbId, logfileId, metricId, captureId)
    models.db.session.add(new_rep)
    models.db.session.commit()

# Return all replays in the replay table
def getReplayAll():
    rep_list = models.Replay.query.with_entities(Replay.id, Replay.name, Replay.time)
    return rep_list

# Add metric to the metric table
def addMetric(name, path):
    new_metric = models.Metric(name, path)
    models.db.session.add(new_metric)
    models.db.session.commit()

# Return metric associated with provided capture or replay
def getMetric(metricId):
    m = models.Metric.query.filter_by(id=metricId).with_entities(models.Metric.name, models.Metric.path)
    return m

# Add logfile to the logfile table
def addLogfile(name, path):
    new_logfile = models.Logfile(name, path)
    models.db.session.add(new_logfile)
    models.db.session.commit()

# Return logfile associated with provided capture or replay
def getLogfile(logfileId):
    log = models.Logfile.query.filter_by(id=logfileId).with_entities(models.Logfile.name, models.Logfile.path)
    return log
