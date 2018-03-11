import boto3
import pymysql
import botocore
import sys
import capture
import logging
from datetime import datetime
import rds_config
import modelsQuery
from ast import literal_eval
from threading import Timer


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def download_file(captureName, bucketName, fileName):
    s3 = boto3.resource('s3')

    try:
        s3.Bucket(bucketName).download_file(fileName, captureName + " " + "tempLogFile")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The file does not exist.")
        else:
            raise

def startReplay(replayName, captureName, dbName, mode):
    logfile = modelsQuery.getLogFileByCapture(captureName)
    username = rds_config.db_username
    password = rds_config.db_password
    endpoint = capture.get_list_of_instances(dbName)['DBInstances'][0]['Endpoint']['Address']
    status_of_db = capture.get_list_of_instances(dbName)['DBInstances'][0]['DBInstanceStatus']

    metricFileName = replayName + " " + "metric file"

    captureStartTime = modelsQuery.getCaptureStartTime(captureName)
    captureEndTime = modelsQuery.getCaptureEndTime(captureName)
    metricFile = modelsQuery.getCaptureMetric(captureName)
    captureID = modelsQuery.getCaptureID(captureName)
    captureBucket = modelsQuery.getCaptureBucket(captureName)

    modelsQuery.addMetric(metricFileName, captureBucket, None)
    modelsQuery.addReplay(replayName, captureStartTime, captureEndTime, dbName, metricFile, captureID, mode, "active")
    download_file(logfile)

    t2 = Timer(datetime.now(), executeReplay, [replayName, captureName, username, password, dbName, status_of_db, endpoint, metricFile, datetime.now()])
    t2.start()


def executeReplay(replayName, captureName, username, password, dbName, status_of_db, endpoint, metricFile, startTime):
    metricBucket = modelsQuery.getCaptureMetricBucket(captureName)
    with open(captureName + " " + "tempLogFile", 'r') as tempFile:
        for line in tempFile:
            entireList = literal_eval(line)
            for i in range(len(entireList)):
                dict = entireList[i]
                if dict['message'].startswith('Query'):
                    executableQuery = str(dict['message'][7:])
                    if status_of_db == "available":
                        try:
                            conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=dbName,
                                                   connect_timeout=5)
                        except:
                            logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
                            sys.exit()
                        with conn.cursor() as cur:
                            cur.execute("""%s""", executableQuery)

    endTime = datetime.now()
    modelsQuery.updateReplayStatus(replayName, "finished")
    capture.sendMetrics(metricBucket, metricFile, startTime, endTime)
