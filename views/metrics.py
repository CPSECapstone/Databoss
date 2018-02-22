from flask import Blueprint, jsonify, request
from parseMetrics import ParsedMetrics
from models import Metric
from web_app import db

import capture

metrics_api = Blueprint('metrics_api', __name__)

@metrics_api.route("/getMetrics", methods=["GET"])
def getMetrics():
    id = request.args.get('id')
    type = request.args.get('type')

    # get the bucket and file name of the metrics file corresponding with the capture/replay
    if type == 'capture':
        metric = Metric.query.filter(Metric.capture.has(id=id)).first()
    elif type == 'replay':
        metric = Metric.query.filter(Metric.replay.has(id=id)).first()
    else:
        # TODO add error handling
        raise Exception('Unspecified Type')

    metrics = getS3Metrics(metric.bucket, metric.file)

    return jsonify(cpu=metrics.cpuList, cpuTime=metrics.cpuTimeList,
                   readIO=metrics.readIOList, readIOTime=metrics.readIOTimeList,
                   writeIO=metrics.writeIOList, writeIOTime=metrics.writeIOTimeList,
                   memory=metrics.memoryList, memoryTime=metrics.memoryTimeList)

# Helper function to get a metrics file from S3 given a bucket and file name
def getS3Metrics(bucket, file):
    obj = capture.s3.Object(bucket, file).get()
    return ParsedMetrics(obj['Body'].read().decode('utf-8'))

#TODO : move this to models.query.py
def add(name, bucket, file):
    newMetrics = Metric(name=name, bucket=bucket, file=file)
    db.session.add(newMetrics)
    db.session.commit()