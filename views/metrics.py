from flask import Blueprint, jsonify, request
from parseMetrics import ParsedMetrics

metrics_api = Blueprint('metrics_api', __name__)

@metrics_api.route("/getMetrics", methods=["GET"])
def getMetrics():
    # TODO get the file from request instead of hard coding
    metrics = ParsedMetrics("metric_files/metric-file.txt")

    return jsonify(cpu=metrics.cpuList, cpuTime=metrics.cpuTimeList,
                   readIO=metrics.readIOList, readIOTime=metrics.readIOTimeList,
                   writeIO=metrics.writeIOList, writeIOTime=metrics.writeIOTimeList,
                   memory=metrics.memoryList, memoryTime=metrics.memoryTimeList)