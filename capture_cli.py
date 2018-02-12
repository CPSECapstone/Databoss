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



'''name = input("Enter name for capture and replay: ")
captureReplayBucket = createBucketName(name, "capture and replay")

name = input("Enter name for metrics bucket: ")
metricBucket = createBucketName(name, "metrics")


db_name = str(input("Enter RDS database name: "))
allotted_time = input("Enter duration of capture (in minutes): ")'''

captureReplayBucket = "capture-replay-info"
metricBucket = "metric-info"
db_name = "new"

list_of_instances = rds.describe_db_instances(
    DBInstanceIdentifier= db_name
)

# Starting the database instance
status_of_db = list_of_instances['DBInstances'][0]['DBInstanceStatus']

'''
if status_of_db == "stopped":
    start_response = rds.start_db_instance(
        DBInstanceIdentifier= db_name
    )
else:
    start_response = "Starting"

print(start_response + "...")
'''
print("Starting RDS database instance: " + db_name)

'''
# Testing RDS Database
username = str(input("Enter username: "))
password = str(input("Enter password: "))
endpoint = str(input("RDS MySQL endpoint: "))'''

username = "sonaraya"
password = "sonaraya"
endpoint = "new.cpguxfvypxd2.us-west-1.rds.amazonaws.com"

print("Connecting...")

conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=db_name)

print("SUCCESS: Connection to RDS MySQL instance succeeded")

print("Adding value to database table 'Student'")
#id = input("Enter student id: ")
#student_name = str(input("Enter student name: "))

numItems = 0

with conn.cursor() as cur:
    cur.execute("create table IF NOT EXISTS Student ( StudentID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (StudentID))")
    cur.execute('insert into Student (StudentID, Name) values('+generate_number(100)+', "'+generate_word(10)+'")')
    conn.commit()
    cur.execute("select * from Student")
    cur.execute('SELECT event_time, command_type, argument FROM mysql.general_log')
    for row in cur:
        numItems += 1
        print(row)

print(str(numItems) + " items exist in your RDS MySQL table")

'''
if status_of_db == "available":
    stop_response = rds.stop_db_instance(
        DBInstanceIdentifier= db_name
    )
else :
    stop_response = "stopped"

print("Stopping database: " + db_name)
print(stop_response)

all_log_files = rds.describe_db_log_files(
    DBInstanceIdentifier= db_name
)
print(all_log_files)

'''

bucket = s3.Bucket(captureReplayBucket)
print("Printing location...")

for key in bucket.objects.all():
    print(key.key)

client = boto3.client(
        service_name='logs',
        aws_access_key_id = user_key,
        aws_secret_access_key = user_access,
        region_name = loc
    )

cloudwatch = boto3.client(
        service_name='cloudwatch',
        aws_access_key_id = user_key,
        aws_secret_access_key = user_access,
        region_name = loc
    )

time.sleep(60)
client.filter_log_events(
    startTime=datetime.now(),
    endTime=datetime.now() - timedelta(minutes=1)
)

rds_logfile = rds.download_db_log_file_portion(
  DBInstanceIdentifier=db_name,
  LogFileName="general/mysql-general.log",
  Marker='0'
)
print(rds_logfile)

logFile = input("Enter file name for log file: ")
metricFile = input("Enter file name for metric file: ")



dlist = []

print("CPU Utilization: ")
dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                              Statistics=['Average'],
                                              StartTime=datetime.utcnow()-timedelta(minutes=60),
                                              EndTime=datetime.utcnow(),
                                              Period=300,
                                              MetricName='CPUUtilization'))
print("Read: ")
dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                              Statistics=['Average'],
                                              StartTime=datetime.utcnow()-timedelta(minutes=60),
                                              EndTime=datetime.utcnow(),
                                              Period=300,
                                              MetricName='ReadIOPS'))
print("Write: ")
dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                              Statistics=['Average'],
                                              StartTime=datetime.utcnow()-timedelta(minutes=60),
                                              EndTime=datetime.utcnow(),
                                              Period=300,
                                              MetricName='WriteIOPS'))
print("Memory: ")
dlist.append(cloudwatch.get_metric_statistics(Namespace="AWS/RDS",
                                              Statistics=['Average'],
                                              StartTime=datetime.utcnow()-timedelta(minutes=60),
                                              EndTime=datetime.utcnow(),
                                              Period=300,
                                              MetricName='FreeableMemory'))


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)

with open(metricFile, 'w') as metricFileOpened:
    metricFileOpened.write(json.dumps(dlist, cls=MyEncoder))

s3_resource.Object(captureReplayBucket, logFile).put(Body=rds_logfile['LogFileData'], Metadata={'foo':'bar'})
s3.meta.client.upload_file(metricFileOpened.name, metricBucket, metricFileOpened.name)
'''s3_resource.Object(metricBucket, metricFile).put(Body=dlist, Metadata={'foo':'bar'})'''

print("Done!")

rds_logfile = rds.describe_db_log_files(
    DBInstanceIdentifier= db_name
)


