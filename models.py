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

    def __init__(self, dialect, name, host, port, database, username):
        self.dialect = dialect
        self.name = name
        self.host = host
        self.port = port
        self.database = database
        self.username = username

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    bucket = db.Column(db.String(100))
    file = db.Column(db.String(100))
    db.UniqueConstraint(bucket, file)
    capture = db.relationship('Capture', backref='metric', lazy=True, uselist=False)
    replay = db.relationship('Replay', backref='metric', lazy=True, uselist=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'bucket': self.bucket,
            'file': self.file
        }

    def __init__(self, name, path):
        self.name = name
        self.path = path

class Logfile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    bucket = db.Column(db.String(100))
    file = db.Column(db.String(100))
    db.UniqueConstraint(bucket, file)
    capture = db.relationship('Capture', backref='logfile', lazy=True, uselist=False)
    replay = db.relationship('Replay', backref='logfile', lazy=True, uselist=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'bucket': self.bucket,
            'file': self.file
        }

    def __init__(self, name, path):
        self.name = name
        self.path = path

class Capture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    dbId = db.Column(db.Integer, db.ForeignKey('dbconnection.id'), nullable=False)
    logfileId = db.Column(db.Integer, db.ForeignKey('logfile.id'), nullable=False)
    metricId = db.Column(db.Integer, db.ForeignKey('metric.id'), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'dbId': self.dbId,
            'logfileId': self.logfileId,
            'metricId': self.metricId
        }

    def __init__(self, name, startTime, endTime, dbId, logfileId, metricId):
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.dbId = dbId
        self.logfileId = logfileId
        self.metricId = metricId

class Replay(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    dbId = db.Column(db.Integer, db.ForeignKey('dbconnection.id'), nullable=False)
    logfileId = db.Column(db.Integer, db.ForeignKey('logfile.id'), nullable=False)
    metricId = db.Column(db.Integer, db.ForeignKey('metric.id'), nullable=False)
    captureId = db.Column(db.Integer, db.ForeignKey('capture.id'), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'dbId': self.dbId,
            'logfileId': self.logfileId,
            'metricId': self.metricId,
            'captureId': self.captureId
        }

    def __init__(self, name, startTime, endTime, dbId, logfileId, metricId, captureId):
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.dbId = dbId
        self.logfileId = logfileId
        self.metricId = metricId
        self.captureId = captureId
