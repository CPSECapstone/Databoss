from capture import capture_api
from flask import jsonify
from models import Capture
from web_app import db
import modelsQuery

@capture_api.route('/getAll')
def getAllCaptures():
    captures = Capture.query.all()
    return jsonify([i.serialize for i in captures])

def add(name, startTime, endTime, dbId, logfileId, metricId):
    modelsQuery.addCapture(name, startTime, endTime, dbId, logfileId, metricId)