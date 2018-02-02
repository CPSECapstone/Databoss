from flask import jsonify, Blueprint
from models import Replay
from web_app import db

replay_api = Blueprint('replay_api', __name__)

@replay_api.route('/getAll')
def getAllReplays():
    replays = Replay.query.all()
    return jsonify([i.serialize for i in replays])

# TODO add date
def add(name, dbId, logfileId, metricId, captureId):
    newReplay = Replay(name=name, dbId=dbId, logfileId=logfileId, metricId=metricId, captureId=captureId)
    db.session.add(newReplay)
    db.session.commit()

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name = db.Column(db.String(100))
    # time = db.Column(db.DateTime)
    # dbId = db.Column(db.Integer, db.ForeignKey('dbconnection.id'),
    #                  nullable=False)
    # logfileId = db.Column(db.Integer, db.ForeignKey('logfile.id'),
    #                       nullable=False)
    # metricId = db.Column(db.Integer, db.ForeignKey('metric.id'), nullable=False)
    # captureId = db.Column(db.Integer, db.ForeignKey('capture.id'),
    #                       nullable=False)