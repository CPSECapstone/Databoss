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
