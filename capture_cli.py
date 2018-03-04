import boto3
import time
import pymysql
import random
import string
from datetime import timedelta
from datetime import datetime
from time import mktime
import json
import logging
import rds_config
import botocore
import sys
import os
import pprint


user_key = input("Enter access key id: ")
user_access = input("Enter secret key: ")
loc = "us-west-1"
bucket_name = "Capture " + str(time.strftime("%x"))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))

s3 = boto3.client(
    service_name='s3',
    aws_access_key_id=user_key,
    aws_secret_access_key=user_access,
    region_name=loc
)

s3_resource = s3 = boto3.resource(
    service_name = 's3',
    aws_access_key_id = user_key,
    aws_secret_access_key = user_access
)

rds = boto3.client(
    service_name='rds',
    aws_access_key_id=user_key,
    aws_secret_access_key=user_access,
    region_name=loc
)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)


#Function that prints all of a user's database instances
# @app.route('/listDBinstances')
def list_db_instances():
    all_instances = rds.describe_db_instances()
    for i in all_instances['DBInstances']:
        print(i['DBInstanceIdentifier'])

# @app.route('/listbuckets')
def list_buckets():
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    for i in bucket_list:
        print(i)

# Creating 2 buckets if they don't already exist
def createBucket(bucketName):
    if (s3_resource.Bucket(bucketName) in s3_resource.buckets.all()):
        print("Found " + bucketName + " bucket")
        return s3_resource.Bucket(bucketName)
    else :
        return s3.create_bucket(
            Bucket=bucketName,
            CreateBucketConfiguration={
            'LocationConstraint': loc}
    )
    #print("Created " + bucketName + " bucket")

#used for creating queries for db
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
        return str(random.randint(0, numLength))

    #creating bucket names
def createBucketName(bucketName, string):
    try:
        captureReplayBucket=createBucket(bucketName)
        print("Created " + bucketName + " bucket")
        return bucketName
    except:
        #bucketName = -1
        testBucketName(bucketName, string)
        #return -1

def testBucketName(bucketName, string):
    print("Change name of bucket")
    name = input("Enter name for " + string + " bucket: ")
    bucketName = createBucketName(name, string)


captureReplayBucket = "capture-replay-info"
metricBucket = "metric-info"
db_name = "new"

list_of_instances = rds.describe_db_instances(
    DBInstanceIdentifier= db_name
)


cloudwatch = boto3.client(
        service_name='cloudwatch',
        aws_access_key_id = user_key,
        aws_secret_access_key = user_access,
        region_name = loc
    )

# Starting the database instance
status_of_db = list_of_instances['DBInstances'][0]['DBInstanceStatus']


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

def get_list_of_instances(db_name):
    list_of_instances = rds.describe_db_instances(
        DBInstanceIdentifier=db_name
    )
    print(list_of_instances)
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



def startCapture():
    print("starting capture")
    db_name = rds_config.db_name
    status_of_db = get_list_of_instances(db_name)['DBInstances'][0]['DBInstanceStatus']

    if status_of_db != "available":
        rds.start_db_instance(
            DBInstanceIdentifier=db_name
        )

def stopCapture(startTime, endTime, captureBucket, metricBucket, captureFileName, metricFileName):
    username = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name
    endpoint = get_list_of_instances(db_name)['DBInstances'][0]['Endpoint']['Address']

    print("username: " + username)
    print("password: " + password)
    print("db_name: " + db_name)
    print(get_list_of_instances(db_name)['DBInstances'][0]['Endpoint']['Address'])

    try:
        conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=db_name, connect_timeout=5)
    except:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()

    with conn.cursor() as cur:

        cur.execute("""SELECT event_time, command_type, argument FROM mysql.general_log""")


        #for row in cur:
            #print(row)

        logfile = list(map(parseRow, cur))
        print(logfile)



        conn.close()

    with open(captureFileName, 'w') as outfile:
        outfile.write(json.dumps(logfile, cls=MyEncoder))

        '''
    with open(captureFileName, 'w') as outfile:
        for item in logfile:
            #print(item)
            outfile.write("%s\n" % item)'''

    s3.meta.client.upload_file(outfile.name, captureBucket, outfile.name)
    #if os.path.exists(captureFileName):
    #    os.remove(captureFileName)

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

    with open(metricFileName, 'w') as metricFileOpened:
        metricFileOpened.write(json.dumps(dlist, cls=MyEncoder))

    s3.meta.client.upload_file(metricFileOpened.name, metricBucket, metricFileOpened.name)
    #if os.path.exists(metricFileName):
    #    os.remove(metricFileName)

startTime = datetime.now() - timedelta(minutes=60)
endTime = datetime.now()


print(startTime)
print(endTime)

res = get_list_of_instances("new")
pprint.pprint(res, width=1)
#startCapture()
#stopCapture(startTime, endTime, captureReplayBucket, metricBucket, "capture", "metrics")
print("done")


