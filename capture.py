import boto3
import time
import pymysql
import botocore
import random
import sys
import string
import logging
from flask import Blueprint, jsonify
from datetime import timedelta
from datetime import datetime
from time import mktime
import rds_config
import modelsQuery

VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))

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


# Configure boto3 to use access/secret key for s3 and rds
def aws_config():
    global s3
    global s3_resource
    global rds

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
    db_identifiers = []
    all_instances = rds.describe_db_instances()

    for i in all_instances['DBInstances']:
        print(i['DBInstanceIdentifier'])
        db_identifiers.append({'name': i['DBInstanceIdentifier']})
    return jsonify(all_instances['DBInstances'])


@capture_api.route('/listbuckets')
def list_buckets():
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    for i in bucket_list:
        print(i)
    return jsonify(bucket_list)


# Creating 2 buckets if they don't already exist
#@app.route()
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


def generate_word(wordLength):
    word = ""
    for i in range(wordLength):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return word


def generate_number(numLength):
    for i in range(numLength):
        return random.randint(numLength)


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
    db_name = rds_config.db_name
    if (storage_limit > storage_max_db):
        print("ERROR: Storage specified is greater than what", db_name, "has allocated")
        sys.exit()
    else:
        parseJson(cloudwatch.get_metric_statistics(Namespace = 'AWS/RDS',
                                    MetricName = 'FreeStorageSpace',
                                    StartTime=datetime.utcnow() - timedelta(minutes=60),
                                    EndTime=datetime.utcnow(),
                                    Period= 300,
                                    Statistics=['Average']
                                        ), storage_limit)

def startCapture(captureName, captureBucket, metricsBucket, db_name, startDate, endDate, startTime, endTime, storage_limit):
    status_of_db = get_list_of_instances(db_name)['DBInstances'][0]['DBInstanceStatus']
    storage_max_db = get_list_of_instances(db_name)['DBInstances'][0]['AllocatedStorage']
    endpoint = get_list_of_instances(db_name)['DBInstances'][0]['Endpoint']['Address']
    port = get_list_of_instances(db_name)['DBInstances'][0]['Endpoint']['Port']
    captureFileName = captureName + " " + "capture file"
    metricFileName = captureName + " " + "metric file"
    dbDialect = "mysql"
    username = rds_config.db_username

    if (startDate == "" and endDate == "" and startTime == "" and endTime == ""):
        startDate = datetime.now().date()
        endDate = datetime.now().date() + timedelta(days=1)
        startTime = datetime.now().time()
        endTime = datetime.now().time()

    sTimeCombined = datetime.combine(startDate, startTime)
    eTimeCombined = datetime.combine(endDate, endTime)


    if status_of_db != "available":
        rds.start_db_instance(
            DBInstanceIdentifier=db_name
        )
    else:
        if storage_limit != None:
            checkStorageCapacity(storage_limit, storage_max_db)

    modelsQuery.addLogfile(captureFileName, captureBucket, None)
    modelsQuery.addMetric(metricFileName, metricsBucket, None)
    print("Type of db_name: ")
    print(type(db_name))
    metricID = modelsQuery.getMetricIDByNameAndBucket(metricFileName, metricsBucket)
    logfileID = modelsQuery.getLogFileIdByNameAndBucket(captureFileName, captureBucket)
    modelsQuery.addDBConnection(dbDialect, db_name, endpoint, port, "", username)


    allDBConnections = modelsQuery.getDBConnectionAll()
    print(allDBConnections)
    modelsQuery.addCapture(captureName, sTimeCombined, eTimeCombined, str(db_name), logfileID, metricID)

def stopCapture(startTime, endTime, captureName, captureBucket, metricBucket, captureFileName, metricFileName):
    captureFileName = captureName + " " + "capture file"
    metricFileName = captureName + " " + "metric file"
    username = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name
    endpoint = get_list_of_instances(db_name)['DBInstances'][0]['Endpoint']['Address']
    status_of_db = get_list_of_instances(db_name)['DBInstances'][0]['DBInstanceStatus']

    if status_of_db == "available":
        try:
            conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=db_name, connect_timeout=5)
        except:
            logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
            sys.exit()
        with conn.cursor() as cur:
            cur.execute("""SELECT event_time, command_type, argument FROM mysql.general_log\
                            WHERE event_time BETWEEN '%s' AND '%s'""" % (startTime, endTime))
            logfile = list(map(parseRow, cur))

            conn.close()

        file = modelsQuery.getLogFile(captureFileName, captureBucket)
        outfile = open(file, 'w')
        for item in logfile:
            outfile.write("%s\n" % item)


        s3.meta.client.upload_file(outfile.name, captureBucket, outfile.name)
        if os.path.exists(captureFileName):
            os.remove(captureFileName)

        sendMetrics(metricBucket, metricFileName)


def sendMetrics(metricBucket, metricFileName):
    dlist = []

    dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                                  Statistics=['Average'],
                                                  StartTime=datetime.utcnow() - timedelta(minutes=60),
                                                  EndTime=datetime.utcnow(),
                                                  Period=300,
                                                  MetricName='CPUUtilization'))

    dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                                  Statistics=['Average'],
                                                  StartTime=datetime.utcnow() - timedelta(minutes=60),
                                                  EndTime=datetime.utcnow(),
                                                  Period=300,
                                                  MetricName='ReadIOPS'))

    dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                                  Statistics=['Average'],
                                                  StartTime=datetime.utcnow() - timedelta(minutes=60),
                                                  EndTime=datetime.utcnow(),
                                                  Period=300,
                                                  MetricName='WriteIOPS'))

    dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                                  Statistics=['Average'],
                                                  StartTime=datetime.utcnow() - timedelta(minutes=60),
                                                  EndTime=datetime.utcnow(),
                                                  Period=300,
                                                  MetricName='FreeableMemory'))

    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return int(mktime(obj.timetuple()))
            return json.JSONEncoder.default(self, obj)

    with open(metricFileName, 'w') as metricFileOpened:
        metricFileOpened.write(json.dumps(dlist, cls=MyEncoder))

    s3.meta.client.upload_file(metricFileOpened.name, metricBucket, metricFileOpened.name)
    if os.path.exists(metricFileName):
        os.remove(metricFileName)


# configures aws credentials when app starts so they don't have to be input manually
# TODO remove when done testing
import json
import os.path

if os.path.exists("credentials.json"):
    credentialFile = open("credentials.json", "r")
    credentials = json.load(credentialFile)
    access_key = credentials['access']
    secret_key = credentials['secret']
    aws_config()