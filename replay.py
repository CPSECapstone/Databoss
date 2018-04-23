import boto3
import pymysql
import botocore
import sys
import capture
import logging
from datetime import datetime
import modelsQuery
from ast import literal_eval
from threading import Timer
import json
import os.path
import sys


logger = logging.getLogger()
logger.setLevel(logging.INFO)


inProgressReplays = []


def addInProgressReplay(replayName, username, password):
    inProgressReplays.append({'replayName': replayName, 'username': username, 'password': password})


def getInProgressReplay(replayName):
    for replay in inProgressReplays:
        if replay.get('replayName') == replayName:
            return replay

    return None


def removeInProgressReplay(replayName):
    for replay in inProgressReplays:
        if replay.get('replayName') == replayName:
            inProgressReplays.remove(replay)

def download_file(replayName, bucketName, fileName):
    try:
        capture.s3.Bucket(bucketName).download_file(fileName, replayName + " " + "tempLogFile")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The file does not exist.")
        else:
            raise

def startReplay(replayName, captureObj, dbName, mode, username, password):
    captureObj = json.loads(captureObj)
    print(captureObj)
    captureName = captureObj['name']
    print("name: " + captureName)
    logfile = modelsQuery.getLogFileByCapture(captureName)
    rdsInstance = captureObj['dbName'].split("/")[0]
    endpoint = capture.get_list_of_instances(rdsInstance)['DBInstances'][0]['Endpoint']['Address']
    status_of_db = capture.get_list_of_instances(rdsInstance)['DBInstances'][0]['DBInstanceStatus']

    metricFileName = replayName + " " + "metric file"

    captureStartTime = modelsQuery.getCaptureStartTime(captureName)
    captureEndTime = modelsQuery.getCaptureEndTime(captureName)
    metricFile = modelsQuery.getCaptureMetric(captureName)
    captureID = modelsQuery.getCaptureID(captureName)
    captureBucket = modelsQuery.getCaptureBucket(captureName)
    metricBucket = modelsQuery.getMetricBucketByName(captureName)
    filename = logfile.filename

    modelsQuery.addMetric(metricFileName, metricBucket, None)
    metricID = modelsQuery.getMetricIDByNameAndBucket(metricFileName, metricBucket)

    ## how to get the current time of the system.
    replayStartTime = datetime.now()
    replayEndTime = datetime.now()
    print("Capture start time: " + captureStartTime.strftime('%m/%d/%Y :%H:%M'))
    print("Current system time: " + replayStartTime.strftime('%m/%d/%Y% :H:%M'))

    modelsQuery.addReplay(replayName, replayStartTime, replayEndTime, dbName, metricID, captureID, mode, "active")
    download_file(captureName, captureBucket, filename)

    addInProgressReplay(replayName, username, password)

    t2 = Timer(0, executeReplay, [replayName, captureName, dbName, status_of_db, endpoint, metricFile, datetime.now()])
    t2.start()

def executeReplay(replayName, captureName, dbName, status_of_db, endpoint, metricFile, startTime):
    print("capture name here: " + captureName)
    print("db name: "  + dbName)
    metricBucket = modelsQuery.getCaptureMetricBucket(captureName)
    inProgressReplay = getInProgressReplay(replayName)
    username = inProgressReplay.get('username')
    password = inProgressReplay.get('password')

    numQueriesExecuted = 0

    with open(captureName + " " + "tempLogFile", 'r') as tempFile:
        for line in tempFile:
            entireList = literal_eval(line)
            for i in range(len(entireList)):
                dict = entireList[i]
                if dict['message'].startswith('Query'):
                    executableQuery = dict['message'][7:]
                    if str(status_of_db) == "available":
                        try:
                            conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=dbName,
                                                   connect_timeout=5)
                        except:
                            logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
                            sys.exit()
                        with conn.cursor() as cur:
                            try:
                                cur.execute(executableQuery)
                                numQueriesExecuted += 1

                            except pymysql.err.OperationalError as err:
                                print(err)
                            except pymysql.err.InternalError as err:
                                print(err)


    if os.path.exists(captureName + " " + "tempLogFile"):
        os.remove(captureName + " " + "tempLogFile")

    endTime = datetime.now()
    modelsQuery.updateReplayStatus(replayName, "finished")
    metricID = modelsQuery.getMetricIDByNameAndBucket(replayName + " " + "metric file", metricBucket)
    capture.sendMetrics(metricID, replayName + " " + "metric file", startTime, endTime)
