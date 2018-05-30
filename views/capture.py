from capture import capture_api
from flask import jsonify, request, Response
import capture
import modelsQuery
from models import Capture, Replay
from datetime import datetime

@capture_api.route('/<name>')
def getCapture(name):
    capture = modelsQuery.getCaptureByName(name)
    return jsonify(capture.serialize)

@capture_api.route('/getAll')
def getAllCaptures():
    captures = Capture.query.all()
    return jsonify([i.serialize for i in captures])

@capture_api.route('/deleteCapture/<id>', methods=["DELETE"])
def deleteCapture(id):
    print("HERHERHEHREHREHRHER")
    result = modelsQuery.removeFinishedCapture(id)
    print("id is " + id)
    return " "

@capture_api.route('/getCapturesWithBuckets')
def getCapturesWithBuckets():
    capturesWithBuckets = modelsQuery.getCapturesWithBuckets()
    jsonifiedCaptures = []
    for i in capturesWithBuckets:
        jsonifiedCaptures.append({
            "id" : i.Capture.id,
            "name" : i.Capture.name,
            "rds" : i.Capture.dbName,
            "bucket" : i.Logfile.bucket,
            "startTime": i.Capture.startTime,
            "endTime":i.Capture.endTime,
            "mode": i.Capture.mode,
            "status":i.Capture.status
            })
    return jsonify(jsonifiedCaptures)

@capture_api.route('/getSortedCapturesAndReplays')
def getSortedCapturesAndReplays():
    captures = Capture.query.order_by(Capture.startTime.desc()).all()
    replays = Replay.query.order_by(Replay.startTime.desc()).all()

    return jsonify(captures=[i.serialize for i in captures], replays=[i.serialize for i in replays])

@capture_api.route('/finished')
def getFinishedCaptures():
    captures = modelsQuery.getCaptureFinished()
    return jsonify([i.serialize for i in captures])

@capture_api.route('/active')
def getActiveCaptures():
    captures = modelsQuery.getCaptureActive()
    return jsonify([i.serialize for i in captures])

@capture_api.route('/scheduled')
def getScheduledCaptures():
    captures = modelsQuery.getCaptureScheduled()
    return jsonify([i.serialize for i in captures])

def add(name, startTime, endTime, dbName, logfileId, metricId, mode, status):
    modelsQuery.addCapture(name, startTime, endTime, dbName, logfileId, metricId, mode, status)


@capture_api.route('/startCapture', methods=["POST"])
def startCapture():
    data = request.json
    capture.startCapture(data['captureName'], data['captureBucket'], data['metricsBucket'], data['rdsInstance'], data['dbName'],
                 data['username'], data['password'], data['startDate'], data['endDate'], data['startTime'], data['endTime'], data['storageNum'],
                 data['storageType'], data['mode'])
    return ""


@capture_api.route('/endCapture', methods=["POST"])
def endCapture():
    data = request.json
    print("comes in end cap & prints data:")
    print(data)
    captureName = data.get('name')
    dbName = data.get('dbName')
    rdsInstance, database = dbName.split("/")
    startTime = data.get('startTime')
    captureBucket = data.get('logfileId')
    metricBucket = data.get('metricId')
    captureFileName = data.get('captureFileName')
    metricFileName = data.get('metricFileName')
    mode = data.get('mode')
    endTime = datetime.now()

    capture.stopCapture(mode, rdsInstance, database, startTime, endTime, captureName,
                captureBucket, metricBucket, captureFileName, metricFileName)

    return "ok"


@capture_api.route('/checkName', methods=["GET"])
def checkName():
    name = request.args.get('name')
    name = name.strip()

    captureId = modelsQuery.getCaptureID(name)

    if captureId is None:
        return "true"
    return "false"
