from flask import Blueprint, jsonify
import parseMetrics

metrics_api = Blueprint('metrics_api', __name__)


@metrics_api.route("/getCPU", methods=["GET"])
def getCPUMetrics():
    if len(parseMetrics.cpuList) == 0 and len(parseMetrics.cpuTimeList) == 0:
        openFile = parseMetrics.readMetricsFile("metric_files/metric-file.txt")
        parseMetrics.createCPULists(openFile)
        parseMetrics._sortLists(parseMetrics.cpuList, parseMetrics.cpuTimeList)

    return jsonify(cpu=parseMetrics.cpuList, cpuTime=parseMetrics.cpuTimeList)


