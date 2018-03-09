from capture import capture_api
from flask import jsonify, request
from capture import startCapture, stopCapture
from models import Capture
import modelsQuery
from models import Capture

@capture_api.route('/<name>')
def getCapture(name):
    print(name)
    capture = modelsQuery.getCaptureByName(name)
    return jsonify(capture.serialize)

@capture_api.route('/getAll')
def getAllCaptures():
    captures = Capture.query.all()
    return jsonify([i.serialize for i in captures])

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
    startCapture(data['captureName'], data['captureBucket'], data['metricsBucket'], data['rdsInstance'], data['dbName'],
                 data['username'], data['password'], data['startDate'], data['endDate'], data['startTime'], data['endTime'],
                 None, data['mode'])
    return {}


@capture_api.route('/endCapture', methods=["POST"])
def endCapture():
    data = request.json
    print(data)
    captureName = data.get('name')
    dbName = data.get('dbName')

    rdsInstance, database = dbName.split("/")

    startTime = data.get('startTime')
    endTime = data.get('endTime')
    captureBucket = data.get('logfileId')
    metricBucket = data.get('metricId')
    captureFileName = data.get('captureFileName')
    metricFileName = data.get('metricFileName')

    stopCapture(rdsInstance, database, startTime, endTime, captureName,
                captureBucket, metricBucket, captureFileName, metricFileName)

    return "ok"
