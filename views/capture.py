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


def add(name, startTime, endTime, dbName, logfileId, metricId, mode, status):
    modelsQuery.addCapture(name, startTime, endTime, dbName, logfileId, metricId, mode, status)


@capture_api.route('/startCapture', methods=["POST"])
def captureRoute():
    data = request.json
    print(data)
    captureName = data['captureName']
    captureBucket = data['captureBucket']
    metricsBucket = data['metricsBucket']
    dbName = data['dbName']
    captureMode = data['mode']
    startDate = data['startDate']
    endDate = data['endDate']
    startTime = data['startTime']
    endTime = data['endTime']

    startCapture(captureName, captureBucket, metricsBucket, dbName, startDate, endDate, startTime, endTime, None, captureMode)
    return "ok"

@capture_api.route('/endCapture', methods=["POST"])
def endCapture():
    data = request.json
    print(data)
    captureName = data.get('name')
    dbName = data.get('dbName')

    startTime = data.get('startTime')
    endTime = data.get('endTime')
    captureBucket = data.get('logfileId')
    metricBucket = data.get('metricId')
    captureFileName = data.get('captureFileName')
    metricFileName = data.get('metricFileName')

    stopCapture(startTime, endTime, captureName, captureBucket, metricBucket, captureFileName, metricFileName)
    return "ok"