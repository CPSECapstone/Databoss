from flask import jsonify, Blueprint, request
import replay
from models import Replay
from web_app import db
import modelsQuery

replay_api = Blueprint('replay_api', __name__)

@replay_api.route('/getAll')
def getAllReplays():
   replays = Replay.query.all()
   return jsonify([i.serialize for i in replays])

def add(name, startTime, endTime, dbName, logfileId, metricId, captureId):
   modelsQuery.addReplay(name, startTime, endTime, dbName, logfileId, metricId, captureId)

@replay_api.route('/startReplay', methods=["POST"])
def startReplay():
    data = request.json
    print(data)
    replay.startReplay(data['replayName'], data['capture'], data['dbName'], data['replayMode'], data['username'], data['password'])
    return ""