import boto3
import time
import pymysql
import getpass

user_key = input("Enter access key id: ")
user_access = input("Enter secret key: ")
loc = "us-west-1"
bucket_name = "Capture " + str(time.strftime("%x"))

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

#creating bucket names
def createBucketName(bucketName):
    try:
        captureReplayBucket=createBucket(bucketName)
    except:
        return -1


name = input("Enter name for capture and replay: ")
captureReplayBucket = createBucketName(name)
while (captureReplayBucket == -1):
    print("Change name of bucket")
    name = input("Enter name for capture and replay: ")
    captureReplayBucket = createBucketName(name)
print("Created " + name + " bucket")

name = input("Enter name for metrics bucket: ")
metricBucket = createBucketName(name)
while (metricBucket == -1):
    print("Change name of bucket")
    name = input("Enter name for metrics bucket: ")
    metricBucket = createBucketName(name)
print("Created " + name + " bucket")


db_name = str(input("Enter RDS database name: "))
allotted_time = input("Enter duration of capture (in minutes): ")

list_of_instances = rds.describe_db_instances(
    DBInstanceIdentifier= db_name
)
print(list_of_instances)

# Starting the database instance
status_of_db = list_of_instances['DBInstances'][0]['DBInstanceStatus']

if status_of_db == "stopped":
    start_response = rds.start_db_instance(
        DBInstanceIdentifier= db_name
    )
else :
    start_response = "Starting"

print("Starting RDS database instance: " + db_name)
print(start_response)

# Testing RDS Database
username = str(input("Enter username: "))
password = str(getpass.getpass(prompt="Enter password: "))
endpoint = str(input("RDS MySQL endpoint: "))

print("Connecting...")

conn = pymysql.connect(host=endpoint, port=3306, user=username, passwd=password, db=db_name)

print("SUCCESS: Connection to RDS MySQL instance succeeded")

print("Adding value to database table 'Student'")
id = input("Enter student id: ")
student_name = str(input("Enter student name: "))

numItems = 0

with conn.cursor() as cur:
    cur.execute("create table IF NOT EXISTS Student ( StudentID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (StudentID))")
    cur.execute('insert into Student (StudentID, Name) values(5, "random")')
    conn.commit()
    cur.execute("select * from Student")
    for row in cur:
        numItems += 1
        print(row)

print("Added " + str(numItems) + " items to RDS MySQL table")

'''
if status_of_db == "available":
    stop_response = rds.stop_db_instance(
        DBInstanceIdentifier= db_name
    )
else :
    stop_response = "stopped"

print("Stopping database: " + db_name)
print(stop_response)
'''
all_log_files = rds.describe_db_log_files(
    DBInstanceIdentifier= db_name
)
print(all_log_files)

'''
rds_logfile = rds.download_db_log_file_portion(
    DBInstanceIdentifier= db_name,
    LogFileName='testing log file',
    Marker='string',
    NumberOfLines=123
)'''