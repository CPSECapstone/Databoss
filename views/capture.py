from capture import capture_api
from flask import jsonify, request
from models import Capture
from capture import startCapture
from web_app import db
import modelsQuery

@capture_api.route('/<id>')
def getCapture(id):
    capture = Capture.query.get(id)
    return jsonify(capture.serialize)

@capture_api.route('/getAll')
def getAllCaptures():
    captures = Capture.query.all()
    return jsonify([i.serialize for i in captures])

def add(name, startTime, endTime, dbName, logfileId, metricId):
    modelsQuery.addCapture(name, startTime, endTime, dbName, logfileId, metricId)


@capture_api.route('/startCapture', methods=["POST"])
def captureRoute():
    data = request.json

    captureName = data['captureName']
    captureBucket = data['captureBucket']
    metricsBucket = data['metricsBucket']
    dbName = data['dbName']
    captureMode = data['captureMode']
    startDate = data['startDate']
    endDate = data['endDate']
    startTime = data['startTime']
    endTime = data['endTime']

    startCapture(captureName, captureBucket, metricsBucket, dbName, startDate, endDate, startTime, endTime, None)