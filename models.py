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


class Workload(db.Model):
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
    workloadId = db.Column(db.Integer, db.ForeignKey('workload.id'), nullable=False)
    metricId = db.Column(db.Integer, db.ForeignKey('metric.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': self.time,
            'dbId': self.dbId,
            'logfileId': self.logfileId,
            'workloadId': self.workloadId,
            'metricId': self.metricId
        }

class Replay(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    dbId = db.Column(db.Integer, db.ForeignKey('dbconnection.id'), nullable=False)
    logfileId = db.Column(db.Integer, db.ForeignKey('logfile.id'), nullable=False)
    workloadId = db.Column(db.Integer, db.ForeignKey('workload.id'), nullable=False)
    metricId = db.Column(db.Integer, db.ForeignKey('metric.id'))
    captureId = db.Column(db.Integer, db.ForeignKey('capture.id'), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': self.time,
            'dbId': self.dbId,
            'logfileId': self.logfileId,
            'workloadId': self.workloadId,
            'metricId': self.metricId,
            'captureId': self.captureId
        }

# Sets up the tables in the database and their connections. Should be called only once.
def createTable():
    db.create_all()
    db.session.commit()

# Return all captures in the capture table
def getCaptureAll():
    capList = Capture.query.with_entities(Capture.id, Capture.name, Capture.time)
    return capList

# Return all replays in the replay table
def getReplayAll():
    repList = Replay.query.with_entities(Replay.id, Replay.name, Replay.time)
    return repList

# Add metric to the metric table
def addMetric(name, path):
    newMetric = Metric(name, path)
    db.session.add(newMetric)
    db.session.commit()

# Return metric associated with provided capture or replay
def getMetric(metricId):
    m = Metric.query.filter_by(id=metricId).with_entities(Metric.name, Metric.path)
    return m

