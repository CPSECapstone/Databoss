from flask import Blueprint, jsonify, request
from parseMetrics import ParsedMetrics
from web_app import db
from models import Capture, Replay

import capture

metrics_api = Blueprint('metrics_api', __name__)

@metrics_api.route("/getMetrics", methods=["GET"])
def getMetrics():
    # TODO get the bucket & file name from request instead of hard coding
    id = request.args.id

    # TODO grab metrics path instead of just cap/rep id
    if request.args.type == 'capture':
        capture = Capture.query.filter_by(id=id)
    elif request.args.type == 'replay':
        replay = Replay.query.filter_by(id=id)

    metrics = getS3MetricsFile("crt-metrics-test", "metric-file.txt")

    return jsonify(cpu=metrics.cpuList, cpuTime=metrics.cpuTimeList,
                   readIO=metrics.readIOList, readIOTime=metrics.readIOTimeList,
                   writeIO=metrics.writeIOList, writeIOTime=metrics.writeIOTimeList,
                   memory=metrics.memoryList, memoryTime=metrics.memoryTimeList)

# Helper function to get a metrics file from S3 given a bucket and file name
def getS3MetricsFile(bucket, file):
    obj = capture.s3_resource.Object(bucket, file).get()
    return ParsedMetrics(obj['Body'].read().decode('utf-8'))