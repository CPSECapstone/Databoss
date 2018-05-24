import boto3
import time
import pymysql
import pymysql.cursors
import botocore
import random
import sys
import string
import logging
from flask import Blueprint, jsonify, request
from datetime import timedelta
from datetime import datetime
from time import mktime
import modelsQuery
import scheduler
import json
import pytz
import os.path
from flask import Response, abort

MAX_CONVERSION = (10**3)
STORAGE_CONVERSION = (10**6)

capture_api = Blueprint('capture_api', __name__)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

access_key = None
secret_key = None

loc = "us-west-1"
bucket_name = "Capture " + str(time.strftime("%x"))

s3 = None
s3_resource = None
rds = None
cloudwatch = None

captureReplayBucket = None
metricBucket = None

inProgressCaptures = []


def addInProgressCapture(captureName, username, password):
    inProgressCaptures.append({'captureName': captureName, 'username': username, 'password': password})


def getInProgressCapture(captureName):
    for capture in inProgressCaptures:
        if capture.get('captureName') == captureName:
            return capture

    return None


def removeInProgressCapture(captureName):
    for capture in inProgressCaptures:
        if capture.get('captureName') == captureName:
            inProgressCaptures.remove(capture)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)


# Configure boto3 to use access/secret key for s3 and rds
def aws_config():
    global s3
    global s3_resource
    global rds
    global cloudwatch

    s3 = boto3.client(
        service_name='s3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=loc
    )

    s3_resource = s3 = boto3.resource(
        service_name='s3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    rds = boto3.client(
        service_name='rds',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=loc
    )

    cloudwatch = boto3.client(
        service_name='cloudwatch',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=loc
    )


# Function that prints all of a user's database instances
@capture_api.route('/listDBinstances')
def list_db_instances():
    all_instances = rds.describe_db_instances()
    return jsonify(all_instances['DBInstances'])


# Route to get all the databases for a given RDS Endpoint
@capture_api.route('/listInstanceDbs/<endpointString>', methods=['POST'])
def list_instance_dbs(endpointString):
    data = request.json
    username = data.get('username')
    password = data.get('password')
    endpoint = json.loads(endpointString)
    host = endpoint.get('Address')
    port = endpoint.get('Port')

    # Connect to the database
    connection = pymysql.connect(host=host,
                                 user=username,
                                 port=port,
                                 password=password)

    try:
        with connection.cursor() as cursor:
            cursor.execute("show databases")
            result = cursor.fetchall()

            result = [i[0] for i in result]
    finally:
        connection.close()

    return jsonify(result)


@capture_api.route('/listbuckets')
def list_buckets():
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    return jsonify(bucket_list)


# Creating 2 buckets if they don't already exist
def createBucket(bucketName):
    if s3_resource.Bucket(bucketName) in s3_resource.buckets.all():
        print("Found " + bucketName + " bucket")
        return s3_resource.Bucket(bucketName)
    else:
        return s3.create_bucket(
            Bucket=bucketName,
            CreateBucketConfiguration={
                'LocationConstraint': loc}
        )


def createBucketName(bucketName, string):
    try:
        captureReplayBucket = createBucket(bucketName)
        print("Created " + bucketName + " bucket")
        return bucketName
    except:
        # bucketName = -1
        testBucketName(bucketName, string)
        # return -1


def testBucketName(bucketName, string):
    print("Change name of bucket")
    name = input("Enter name for " + string + " bucket: ")
    bucketName = createBucketName(name, string)


def get_list_of_instances(db_name):
    list_of_instances = rds.describe_db_instances(
        DBInstanceIdentifier=db_name
    )
    return list_of_instances

def get_log_file(bucket_name, file_name):
    s3 = boto3.resource('s3')

    try:
        s3.Bucket(bucket_name).download_file(file_name, 'local-file.txt')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("Object does not exist in bucket.")
        else:
            raise e

def parseRow(row):
    eventTime = row[0]
    command = row[1]
    query = row[2]

    if hasattr(query, 'decode'):
        query = query.decode()

    message = command + ": " + query

    return {
        'timestamp': eventTime,
        'message': message
    }


def parseJson(jsonString, storage_limit):
    freeSpace = (jsonString['Datapoints'][0]['Average'])/(10 **9)
    if (storage_limit > freeSpace):
        logger.error("ERROR: Not enough space for this.")
        sys.exit()
    else:
        storageRem = freeSpace - storage_limit
        for element in jsonString['Datapoints'][1:]:
            gbVal = (element['Average'])/(10 ** 9)
            #if (gbVal <= storageRem):   #Storage limit has been met
                #CALL stopCapture()


#storage_limit should be in gb
def checkStorageCapacity(storage_limit, storage_max_db):
    if (storage_limit > storage_max_db):
        sys.exit()
    else:
        parseJson(cloudwatch.get_metric_statistics(Namespace = 'AWS/RDS',
                                    MetricName = 'FreeStorageSpace',
                                    StartTime=datetime.utcnow() - timedelta(minutes=60),
                                    EndTime=datetime.utcnow(),
                                    Period= 300,
                                    Statistics=['Average']
                                        ), storage_limit)


def updateDatabase(sTime, eTime, cName, cBucket, mBucket, cFile, mFile, dialect, rdsInstance, dbName, port, username, mode, status):
    endpoint = get_list_of_instances(rdsInstance)['DBInstances'][0]['Endpoint']['Address']
    modelsQuery.addLogfile(cFile, cBucket, None)
    modelsQuery.addMetric(mFile, mBucket, None)
    modelsQuery.addDBConnection(dialect, str(rdsInstance + "/" + dbName), endpoint, port, dbName, username)
    metricID = modelsQuery.getMetricIDByNameAndBucket(mFile, mBucket)
    logfileID = modelsQuery.getLogFileIdByNameAndBucket(cFile, cBucket)
    modelsQuery.addCapture(cName, sTime, eTime, str(rdsInstance + "/" + dbName), logfileID, metricID, mode, status)


def startCapture(captureName, captureBucket, metricsBucket, rdsInstance, db_name, username, password,
                 startDate, endDate, startTime, endTime, storageNum, storageType, mode):
    status_of_db = get_list_of_instances(rdsInstance)['DBInstances'][0]['DBInstanceStatus']
    storage_max_db = get_list_of_instances(rdsInstance)['DBInstances'][0]['AllocatedStorage']
    storage_max_db = storage_max_db * MAX_CONVERSION
    print("Storage max db: " + str(storage_max_db))
    port = get_list_of_instances(rdsInstance)['DBInstances'][0]['Endpoint']['Port']

    captureFileName = captureName + " " + "capture file"
    metricFileName = captureName + " " + "metric file"
    dbDialect = "mysql"

    if mode != "time" or startDate == "" and endDate == "" and startTime == "" and endTime == "":
        startDate = datetime.now().date()
        endDate = datetime.now().date() + timedelta(days=1)
        startTime = datetime.now().time()
        endTime = datetime.now().time()
    else:
        startDate = datetime.strptime(startDate, "%m/%d/%Y").date()
        endDate = datetime.strptime(endDate, "%m/%d/%Y").date()
        startTime = datetime.strptime(startTime, "%H:%M").time()
        endTime = datetime.strptime(endTime, "%H:%M").time()

        print(datetime.combine(startDate, startTime))
        print(datetime.now() + timedelta(minutes=1))
        if datetime.combine(startDate, startTime) < datetime.now() + timedelta(minutes=1):
            startDate = datetime.now().date()
            startTime = (datetime.now() + timedelta(minutes=1)).time()

            if startDate > endDate or startDate == endDate and startTime >= endTime:
                print("Invalid end time when start time is before current time")
                abort(408)

    sTimeCombined = datetime.combine(startDate, startTime)
    eTimeCombined = datetime.combine(endDate, endTime)

    if mode == "time":
        updateDatabase(sTimeCombined, eTimeCombined, captureName, captureBucket, metricsBucket,
                       captureFileName, metricFileName, dbDialect, rdsInstance, db_name, port, username, mode, "scheduled")
        scheduler.scheduleCapture(captureName)

    else:
        if status_of_db != "available":
            rds.start_db_instance(
                DBInstanceIdentifier=rdsInstance
            )
        else:
            if mode == "storage":
                # convert gb to mb
                storage_limit = float(storageNum)
                if (storageType == 'gb-button'):
                    storage_limit = storage_limit * 1000
                    print("storage limit: ", storage_limit)
                if (storage_limit > storage_max_db):
                    print("STORAGE ERROR")
                    abort(400)
                    #return Response("Storage is too large", status=400)
                if (storage_limit <= 0):
                    print("Storage cannot be negative")

                    abort(406)
                    #return Response("Storage cannot be negative", status=406)
                else:

                    updateDatabase(sTimeCombined, eTimeCombined, captureName, captureBucket, metricsBucket,
                               captureFileName, metricFileName, dbDialect, rdsInstance, db_name, port, username, mode,
                               "active")
                    storageMetrics = cloudwatch.get_metric_statistics(Namespace='AWS/RDS',
                                                                              MetricName='FreeStorageSpace',
                                                                              StartTime=datetime.now() - timedelta(
                                                                                  minutes=1),
                                                                              EndTime=datetime.now(),
                                                                              Period=60,
                                                                              Statistics=['Average']
                                                                              )
                    freeSpace = (storageMetrics['Datapoints'][0]['Average']) / (STORAGE_CONVERSION)
                    scheduler.scheduleStorageCapture(datetime.now(), storage_limit, freeSpace, captureName)


        if mode != "storage":
            updateDatabase(sTimeCombined, eTimeCombined, captureName, captureBucket, metricsBucket,
                       captureFileName, metricFileName, dbDialect, rdsInstance, db_name, port, username, mode, "active")
    print("Makes it here")
    addInProgressCapture(captureName, username, password)


def stopCapture(rdsInstance, dbName, startTime, endTime, captureName,
                captureBucket, metricBucket, captureFileName, metricFileName):
    captureFileName = captureName + " " + "capture file"
    metricFileName = captureName + " " + "metric file"

    startTime = datetime.strptime(startTime, '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=pytz.utc).strftime("%Y-%m-%d %H:%M:%S")
    endTime = datetime.strftime(endTime, '%Y-%m-%d %H:%M:%S')

    # Get UTC start and end time for selecting logged queries
    utcStartTime = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
    utcStartTime = pytz.timezone('US/Pacific').localize(utcStartTime).astimezone(pytz.timezone('UTC')).strftime("%Y-%m-%d %H:%M:%S")

    utcEndTime = datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
    utcEndTime = pytz.timezone('US/Pacific').localize(utcEndTime).astimezone(pytz.timezone('UTC')).strftime("%Y-%m-%d %H:%M:%S")

    endpoint = get_list_of_instances(rdsInstance)['DBInstances'][0]['Endpoint']['Address']
    status_of_db = get_list_of_instances(rdsInstance)['DBInstances'][0]['DBInstanceStatus']

    if status_of_db == "available":
        try:
            inProgressCapture = getInProgressCapture(captureName)
            username = inProgressCapture.get('username')
            password = inProgressCapture.get('password')
            conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=dbName, connect_timeout=5)

        except:
            logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
            conn.close()
            sys.exit()
        with conn.cursor() as cur:
            cur.execute("""SELECT event_time, command_type, argument FROM mysql.general_log\
                        WHERE user_host not like '%%rds%%' AND\
                        event_time BETWEEN '%s' AND '%s'""" % (utcStartTime, utcEndTime))
            logfile = list(map(parseRow, cur))
            conn.close()

        with open(captureFileName, 'w') as outfile:
            outfile.write(json.dumps(logfile, cls=MyEncoder))

        bucketCheck = modelsQuery.getCaptureBucket(captureName)

        modelsQuery.updateLogFile(captureBucket, outfile.name)
        s3.meta.client.upload_file(outfile.name, bucketCheck, outfile.name)
        if os.path.exists(captureFileName):
            os.remove(captureFileName)

        parsedEndTime = datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
        modelsQuery.updateCaptureStatus(captureName, "finished")
        modelsQuery.updateCaptureEndTime(captureName, parsedEndTime)
        sendMetrics(metricBucket, metricFileName, startTime, endTime)

        removeInProgressCapture(captureName)


def sendMetrics(metricBucket, metricFileName, startTime, endTime):
    dlist = []

    dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                                  Statistics=['Average'],
                                                  StartTime=startTime,
                                                  EndTime=endTime,
                                                  Period=60,
                                                  MetricName='CPUUtilization'))

    dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                                  Statistics=['Average'],
                                                  StartTime=startTime,
                                                  EndTime=endTime,
                                                  Period=60,
                                                  MetricName='ReadIOPS'))

    dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                                  Statistics=['Average'],
                                                  StartTime=startTime,
                                                  EndTime=endTime,
                                                  Period=60,
                                                  MetricName='WriteIOPS'))

    dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                                  Statistics=['Average'],
                                                  StartTime=startTime,
                                                  EndTime=endTime,
                                                  Period=60,
                                                  MetricName='FreeableMemory'))

    with open(metricFileName, 'w') as metricFileOpened:
        metricFileOpened.write(json.dumps(dlist, cls=MyEncoder))

    modelsQuery.updateMetricFile(metricBucket, metricFileOpened.name)
    s3.meta.client.upload_file(metricFileOpened.name, modelsQuery.getMetricBucket(metricBucket), metricFileOpened.name)
    #metricFileOpened.close()
    if os.path.exists(metricFileName):
        os.remove(metricFileName)



import json
import os.path

if os.path.exists("credentials.json"):
    credentialFile = open("credentials.json", "r")
    credentials = json.load(credentialFile)
    access_key = credentials['access']
    secret_key = credentials['secret']

    aws_config()

