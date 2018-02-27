import boto3
import time
import pymysql
from datetime import timedelta
from datetime import datetime
from time import mktime
import json
import logging
import sys

#initial setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

loc = "us-west-1"
#bucket_name = "Capture " + str(time.strftime("%x"))

s3 = None
s3_resource = None
rds = None
cloudwatch = None
storage_max_db = 0

# Configure boto3 to use access/secret key for s3 and rds
def aws_config(access_key, secret_key):
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


def list_db_instances():
    all_instances = rds.describe_db_instances()
    for i in all_instances['DBInstances']:
        print(i['DBInstanceIdentifier'])


def startRDS(db_name, db_username, db_password, db_endpoint):
    list_of_instances = rds.describe_db_instances(
        DBInstanceIdentifier= db_name
    )
    # Starting the database instance
    status_of_db = list_of_instances['DBInstances'][0]['DBInstanceStatus']
    #this value is in gb
    storage_max_db = list_of_instances['DBInstances'][0]['AllocatedStorage']


    if status_of_db != "available":
        rds.start_db_instance(
            DBInstanceIdentifier=db_name
        )
    else:
        try:
            connection = pymysql.connect(host=db_endpoint, user=db_username, passwd=db_password, db=db_name)
        except:
            logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
            sys.exit()

def parseJson(jsonString, storage_limit):
    freeSpace = (jsonString['Datapoints'][0]['Average'])/(10 **9)
    if (storage_limit > freeSpace):
        logger.error("ERROR: Not enough space for this.")
        return -1
        #sys.exit()
    else:
        storageRem = freeSpace - storage_limit
        for element in jsonString['Datapoints'][1:]:
            gbVal = (element['Average'])/(10 ** 9)
            if (gbVal <= storageRem):
                print('Storage limit has been met')
                #call stop capture here
                return 0
                #sys.exit()

#storage_limit should be in gb
def checkStorageCacity(storage_limit, db_name):
    if (storage_limit > storage_max_db):
        print("ERROR: Storage specified is greater than what", db_name, "has allocated")
        return -1
    else:
        parseJson(cloudwatch.get_metric_statistics(Namespace = 'AWS/RDS',
                                    MetricName = 'FreeStorageSpace',
                                    StartTime=datetime.utcnow() - timedelta(minutes=60),
                                    EndTime=datetime.utcnow(),
                                    Period= 300,
                                    Statistics=['Average']
                                        ), storage_limit)


