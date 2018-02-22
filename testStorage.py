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
import sys

#initial setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)
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

cloudwatch = boto3.client(
        service_name='cloudwatch',
        aws_access_key_id = user_key,
        aws_secret_access_key = user_access,
        region_name = loc
)

username = str(input("enter db username: "))
password = str(input("enter db password: "))
db_name = str(input("Enter RDS database name: "))
endpoint = "storagedb.coircswctb4r.us-west-1.rds.amazonaws.com"

def list_db_instances():
    all_instances = rds.describe_db_instances()
    for i in all_instances['DBInstances']:
        print(i['DBInstanceIdentifier'])

list_of_instances = rds.describe_db_instances(
    DBInstanceIdentifier= db_name
)
# Starting the database instance
status_of_db = list_of_instances['DBInstances'][0]['DBInstanceStatus']
#print("status of db:", status_of_db)

#this value is in gb
storage_max_db = list_of_instances['DBInstances'][0]['AllocatedStorage']


if status_of_db != "available":
    rds.start_db_instance(
        DBInstanceIdentifier=db_name
    )
else:
    try:
        connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=db_name)
    except:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()

def parseJson(jsonString, storage_limit):
    freeSpace = (jsonString['Datapoints'][0]['Average'])/(10 **9)
    if (storage_limit > freeSpace):
        logger.error("ERROR: Not enough space for this.")
        sys.exit()
    else:
        storageRem = freeSpace - storage_limit
        for element in jsonString['Datapoints'][1:]:
            gbVal = (element['Average'])/(10 ** 9)
           # print(gbVal)
            if (gbVal <= storageRem):
                print('Storage limit has been met')
                #call stop capture here
                sys.exit()


#storage_limit should be in gb
def checkStorageCacity(storage_limit):
    if (storage_limit > storage_max_db):
        print("ERROR: Storage specified is greater than what", db_name, "has allocated")
    else:
        parseJson(cloudwatch.get_metric_statistics(Namespace = 'AWS/RDS',
                                    MetricName = 'FreeStorageSpace',
                                    StartTime=datetime.utcnow() - timedelta(minutes=60),
                                    EndTime=datetime.utcnow(),
                                    Period= 300,
                                    Statistics=['Average']
                                        ), storage_limit)




#def

#testing this function
checkStorageCacity(5);