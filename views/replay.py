from flask import jsonify, Blueprint, request
import replay
from models import Replay
from web_app import db
import modelsQuery

replay_api = Blueprint('replay_api', __name__)

@replay_api.route('/<name>')
def getReplay(name):
    replay = modelsQuery.getReplayByName(name)
    return jsonify(replay.serialize)

@replay_api.route('/getAll')
def getAllReplays():
   replays = Replay.query.all()
   return jsonify([i.serialize for i in replays])


@replay_api.route('/deleteReplay/<id>', methods=["DELETE"])
def deleteReplay(id):
    result = modelsQuery.removeFinishedReplay(id)
    print("id is " + id)
    return " "

@replay_api.route('/getReplaysWithBuckets')
def getReplaysWithBuckets():
    replaysWithBuckets = modelsQuery.getReplaysWithBuckets()
    jsonifiedReplays = []
    for i in replaysWithBuckets:
        jsonifiedReplays.append({"id" : i.Replay.id, "name" : i.Replay.name, "rds" : i.Replay.dbName, "bucket" : i.Metric.bucket,
                                 "captureId" : i.Replay.captureId, "startTime": i.Replay.startTime})
    return jsonify(jsonifiedReplays)

def add(name, startTime, endTime, dbName, logfileId, metricId, captureId):
   modelsQuery.addReplay(name, startTime, endTime, dbName, logfileId, metricId, captureId)

@replay_api.route('/startReplay', methods=["POST"])
def startReplay():
    data = request.json
    print(data)
    replay.startReplay(data['replayName'], data['capture'], data['dbName'], data['replayMode'], data['username'], data['password'])
    return ""


@replay_api.route('/checkName', methods=["GET"])
def checkReplayName():
    name = request.args.get('name')
    name = name.strip()

    replay = modelsQuery.getReplayByName(name)

    if replay is None:
        return "true"
    return "false"
