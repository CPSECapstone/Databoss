from capture import capture_api
from flask import jsonify
from models import Capture
from web_app import db

@capture_api.route('/getAll')
def getAllCaptures():
    captures = Capture.query.all()
    return jsonify([i.serialize for i in captures])

def add(name, dbId, logfileId, metricId):
    newCapture = Capture(name=name, dbId=dbId, logfileId=logfileId, metricId=metricId)
    db.session.add(newCapture)
    db.session.commit()