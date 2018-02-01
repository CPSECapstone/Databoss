from web_app import db


class DBConnection(db.Model):
    __tablename__ = "dbconnection"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dialect = db.Column(db.String(25))
    name = db.Column(db.String(100))
    host = db.Column(db.String(100))
    port = db.Column(db.Integer)
    database = db.Column(db.String(100))
    username = db.Column(db.String(100))
    captures = db.relationship('Capture', lazy=True)
    replays = db.relationship('Replay', lazy=True)

    @property
    def serialize(self):
        # """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'dialect': self.dialect,
            'name': self.name,
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'username': self.username
        }

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    path = db.Column(db.String(100), unique=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path
        }

class Logfile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    path = db.Column(db.String(100), unique=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path
        }

class Capture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    dbId = db.Column(db.Integer, db.ForeignKey('dbconnection.id'), nullable=False)
    logfileId = db.Column(db.Integer, db.ForeignKey('logfile.id'), nullable=False)
    metricId = db.Column(db.Integer, db.ForeignKey('metric.id'), nullable=Fales)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': self.time,
            'dbId': self.dbId,
            'logfileId': self.logfileId,
            'metricId': self.metricId
        }

class Replay(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    dbId = db.Column(db.Integer, db.ForeignKey('dbconnection.id'), nullable=False)
    logfileId = db.Column(db.Integer, db.ForeignKey('logfile.id'), nullable=False)
    metricId = db.Column(db.Integer, db.ForeignKey('metric.id'), nullable=False)
    captureId = db.Column(db.Integer, db.ForeignKey('capture.id'), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': self.time,
            'dbId': self.dbId,
            'logfileId': self.logfileId,
            'metricId': self.metricId,
            'captureId': self.captureId
        }

# Sets up the tables in the database and their connections. Should be called only once.
def createTable():
    db.create_all()
    db.session.commit()

# Add capture to capture table with references to associated files
def addCapture(name, time, dbId, logfileId, metricId):
    new_cap = Capture(name, time, dbId, logfileId, metricId)
    db.session.add(new_cap)
    db.session.commit()

# Return all captures in the capture table
def getCaptureAll():
    cap_list = Capture.query.with_entities(Capture.id, Capture.name, Capture.time)
    return cap_list

# Add replay to replay table with references to associated files
def addReplay(name, time, dbId, logfileId, metricId, captureId):
    new_rep = Capture(name, time, dbId, logfileId, metricId, captureId)
    db.session.add(new_rep)
    db.session.commit()

# Return all replays in the replay table
def getReplayAll():
    rep_list = Replay.query.with_entities(Replay.id, Replay.name, Replay.time)
    return rep_list

# Add metric to the metric table
def addMetric(name, path):
    new_metric = Metric(name, path)
    db.session.add(new_metric)
    db.session.commit()

# Return metric associated with provided capture or replay
def getMetric(metricId):
    m = Metric.query.filter_by(id=metricId).with_entities(Metric.name, Metric.path)
    return m

# Add logfile to the logfile table
def addLogfile(name, path):
    new_logfile = Logfile(name, path)
    db.session.add(new_logfile)
    db.session.commit()

# Return logfile associated with provided capture or replay
def getLogfile(logfileId):
    log = Logfile.query.filter_by(id=logfileId).with_entities(Logfile.name, Logfile.path)
    return log
