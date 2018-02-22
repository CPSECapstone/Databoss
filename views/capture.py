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

def add(id, name, startTime, endTime, dbName, logfileId, metricId):
    modelsQuery.addCapture(id, name, startTime, endTime, dbName, logfileId, metricId)


@capture_api.route('/startCapture', methods=["POST"])
def captureRoute():
    data = request.data
    metricsBucket = data[0]
    captureBucket = data[1]
    database = data[2]
    startTime = data[3]
    endTime = data[4]
    startCapture(captureBucket, metricsBucket, database, startTime, endTime, " ")