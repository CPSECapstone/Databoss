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

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def startReplay(replayName, captureName, dbName, startDate, endDate, startTime, endTime, storage_limit, mode):
    print("start replay")
    '''
    logfile = modelsQuery.getLogFileByCapture(captureName)
    username = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name
    endpoint = capture.get_list_of_instances(db_name)['DBInstances'][0]['Endpoint']['Address']
    status_of_db = capture.get_list_of_instances(db_name)['DBInstances'][0]['DBInstanceStatus']

    if status_of_db == "available":
        try:
            conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=db_name, connect_timeout=5)
        except:
            logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
            sys.exit()
        with conn.cursor() as cur:
            cur.execute("""SELECT event_time, command_type, argument FROM mysql.general_log\
                          WHERE argument LIKE '%word1%'""")
            conn.close()

    #get log file that corresponds to the capture
    #connect to database dbName
    #execute queries in file
    #get metrics from cloudwatch
    #update database for a replay
    #modelsQuery.addReplay(replayName, )


    startReplay(data['replayName'], data['captureBucket'], data['dbName'], data['startDate'],
                data['endDate'], data['startTime'], data['endTime'], None, data['mode'])
'''