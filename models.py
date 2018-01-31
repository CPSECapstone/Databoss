from web_app import db


class DBConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dialect = db.Column(db.String(25))
    name = db.Column(db.String(100))
    host = db.Column(db.String(100))
    port = db.Column(db.Integer)
    database = db.Column(db.String(100))
    username = db.Column(db.String(100))

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

class metric(db.Model):
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


class workload(db.Model):
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

class logfile(db.Model):
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

class capture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    dbId = db.Column(db.Integer, db.ForeignKey('DBConnection.id'), nullable=False)
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

class replay(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    dbId = db.Column(db.Integer, db.ForeignKey('DBConnection.id'), nullable=False)
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
    capList = capture.query.with_entities(capture.id, capture.name, capture.time)
    return capList

# Return all replays in the replay table
def getReplayAll():
    repList = replay.query.with_entities(replay.id, replay.name, replay.time)
    return repList

# Add metric to the metric table
def addMetric(name, path):
    newMetric = metric(name, path)
    db.session.add(newMetric)
    db.session.commit()

# Return metric associated with provided capture or replay
def getMetric(metricId):
    m = metric.query.filter_by(id=metricId).all()
    return m

