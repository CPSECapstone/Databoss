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