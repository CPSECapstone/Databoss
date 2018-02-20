from capture import capture_api
from flask import jsonify, request
from models import Capture
from capture import startCapture
import modelsQuery

@capture_api.route('/getAll', methods=['GET'])
def getAllCaptures():
    captures = Capture.query.all()
    return jsonify([i.serialize for i in captures])

def add(name, startTime, endTime, dbId, logfileId, metricId):
    modelsQuery.addCapture(name, startTime, endTime, dbId, logfileId, metricId)

@capture_api.route('/startCapture', methods=['POST'])
def captureRoute():
    data = request.json
    startCapture(data['captureName'], data['captureBucket'], data['metricsBucket'], data['database'], data['captureMode'], data['startDate'], data['endDate'], data['startTime'], data['endTime'], " ")
