import boto3
import time
import pymysql
import botocore
import random
import sys
import string
import logging
from flask import Blueprint, jsonify
import rds_config

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
log_client = None

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

    log_client = boto3.client(
        service_name='logs',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        region_name = loc
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


@capture_api.route('/startCapture')
def startCapture(data):
    username = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name
    status_of_db = get_list_of_instances(db_name)['DBInstances'][0]['DBInstanceStatus']
    endpoint = get_list_of_instances(db_name)['DBInstances'][0]['Endpoint']


    if status_of_db != "available":
        rds.start_db_instance(
            DBInstanceIdentifier=db_name
        )

    else:
        try:
            connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=db_name, connect_timeout=5)
        except:
            logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
            sys.exit()

        with connection.cursor() as cur:
            cur.execute(
                "create table IF NOT EXISTS Student ( StudentID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (StudentID))")
            cur.execute(
                'insert into Student (StudentID, Name) values(' + generate_number(100) + ', "' + generate_word(10) + '")')
            connection.commit()
            cur.execute("select * from Student")
            cur.execute('select * from mysql.general_log')


def stopCapture(startTime, endTime, username, password, db_name, fileName):

    log_client.filter_log_events(
        startTime=startTime,
        endTime=endTime,
    )

    rds_logfile = rds.download_db_log_file_portion(
        DBInstanceIdentifier=db_name,
        LogFileName="general/mysql-general.log",
        Marker='0'
    )
    s3_resource.Object(captureReplayBucket, fileName).put(Body=rds_logfile['LogFileData'], Metadata={'foo': 'bar'})


#import cloudwatchlogs from boto3 client
#def filterLogFile(startTime, endTime) {
#    response = client.filter_log_events(
#        logGroupName='string',
#        logStreamNames=[
#            'string',
 #       ],
 #       startTime=startTime,
 #       endTime=endTime,
 #       filterPattern='string',
 #       nextToken='string',
 #       limit=123,
 #       interleaved=True | False
   # )
#}


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

