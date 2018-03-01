from flask import jsonify, Blueprint, request
from replay import startReplay
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
    dbName = data['dbName']
    startDate = data['startDate']
    endDate = data['endDate']
    startTime = data['startTime']
    endTime = data['endTime']
    replayMode = data['replayMode']

    startReplay(data['replayName'], data['captureBucket'], data['dbName'], data['startDate'],
                data['endDate'], data['startTime'], data['endTime'], None, data['replayMode'])