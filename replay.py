import boto3
import time
import pymysql
import botocore
import random
import sys
import capture
import string
import logging
from flask import Blueprint, jsonify
from datetime import timedelta
from datetime import datetime
from time import mktime
import rds_config
import modelsQuery
from ast import literal_eval

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

def startReplay(replayName, captureName, dbName, startDate, endDate, startTime, endTime, storage_limit, mode):
    logfile = modelsQuery.getLogFileByCapture(captureName)
    username = rds_config.db_username
    password = rds_config.db_password
    endpoint = capture.get_list_of_instances(dbName)['DBInstances'][0]['Endpoint']['Address']
    status_of_db = capture.get_list_of_instances(dbName)['DBInstances'][0]['DBInstanceStatus']

    captureStartTime = modelsQuery.getCaptureStartTime(captureName)
    captureEndTime = modelsQuery.getCaptureEndTime(captureName)


    download_file(logfile)

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
        conn.close()


    #get log file that corresponds to the capture
    #connect to database dbName
    #execute queries in file
    #get metrics from cloudwatch
    #update database for a replay
    #modelsQuery.addReplay(replayName, )
