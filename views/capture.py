from capture import capture_api
from flask import jsonify, request
from capture import startCapture, stopCapture
from models import Capture
import modelsQuery

@capture_api.route('/<name>')
def getCapture(name):
    capture = modelsQuery.getCaptureByName(name)
    return jsonify(capture.serialize)

@capture_api.route('/getAll')
def getAllCaptures():
    captures = Capture.query.all()
    return jsonify([i.serialize for i in captures])

def add(name, startTime, endTime, dbName, logfileId, metricId, mode):
    modelsQuery.addCapture(name, startTime, endTime, dbName, logfileId, metricId, mode)


@capture_api.route('/startCapture', methods=["POST"])
def captureRoute():
    data = request.json

    captureName = data['captureName']
    captureBucket = data['captureBucket']
    metricsBucket = data['metricsBucket']
    dbName = data['dbName']
    startDate = data['startDate']
    endDate = data['endDate']
    startTime = data['startTime']
    endTime = data['endTime']
    mode = data['mode']
    print("THIS IS DA MODE" + mode)

    print(data)
    startCapture(captureName, captureBucket, metricsBucket, dbName, startDate, endDate, startTime, endTime, None, mode)
    return "ok"

@capture_api.route('/endCapture', methods=["POST"])
def endCapture():
    data = request.json
    print(data)
    captureName = data.get('name')
    dbName = data.get('dbName')

    startTime = data.get('startTime')
    endTime = data.get('endTime')
    captureBucket = data.get('captureBucket')
    metricBucket = data.get('metricBucket')
    captureFileName = data.get('captureFileName')
    metricFileName = data.get('metricFileName')
    mode = data.get('mode')

    stopCapture(startTime, endTime, captureName, captureBucket, metricBucket, captureFileName, metricFileName)
