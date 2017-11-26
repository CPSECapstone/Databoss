import boto3
import time
import sys
import pymysql

user_key = input("Enter access key id: ")
user_access = input("Enter secret key: ")

bucket_name = "Capture " + str(time.strftime("%x"))
print(bucket_name)

s3 = boto3.client(
    service_name='s3',
    aws_access_key_id=user_key,
    aws_secret_access_key=user_access,
    region_name='us-west-1'
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
    region_name='us-west-1'
)

if (s3_resource.Bucket('capture-replay-info') in s3_resource.buckets.all()) :
    main_bucket = s3_resource.Bucket('capture-replay-info')
else :
    main_bucket = s3.create_bucket(
        Bucket='capture-replay-info',
        CreateBucketConfiguration={
            'LocationConstraint': 'us-west-1'}
    )

db_name = input("Enter database endpoint: ")

alloted_time = input("Enter duration of capture (in minutes): ")

list_of_instances = rds.describe_db_instances(
    DBInstanceIdentifier= db_name
)

status_of_db = list_of_instances['DBInstances'][0]['DBInstanceStatus']

if status_of_db == "stopped":
    start_response = rds.start_db_instance(
        DBInstanceIdentifier= db_name
    )
else :
    start_response = "starting"

print("Starting database: " + db_name)
print(start_response)

# Testing RDS Database
username = input("Enter username: ")
password = input("Enter password: ")
endpoint = input("RDS MySQL endpoint: ")
port = "3306"

try:
    conn = pymysql.connect(host=endpoint, port=port, user=username, passwd=password, db=db_name, connection_timeout=5)
except:
    print("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

print("SUCCESS: Connection to RDS MySQL instance succeeded")

numItems = 0

with conn.cursor() as cur:
    cur.execute("create table Student ( StudentID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (StudentID))")
    cur.execute('insert into Student (StudentID, Name) values(1, "Joe")')
    cur.execute('insert into Student (StudentID, Name) values(2, "Bob")')
    cur.execute('insert into Student (StudentID, Name) values(3, "Mary")')
    conn.commit()
    cur.execute("select * from Student")
    for row in cur:
        numItems += 1
        print(row)

print("Added" + str(numItems) + "items from RDS MySQL table")

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
rds_logfile = rds.download_db_log_file_portion(
    DBInstanceIdentifier= db_name,
    LogFileName='testing log file',
    Marker='string',
    NumberOfLines=123
)'''