import boto3
import pymysql
import botocore
import sys
import logging
from time import mktime
import modelsQuery
import json
import os.path
from boto3 import Session



#import json
#import os.path

#if os.path.exists("credentials.json"):
#    credentialFile = open("credentials.json", "r")
#    credentials = json.load(credentialFile)
#    access_key = credentials['access']
#    secret_key = credentials['secret']

#iam_resource = boto3.resource(
#        service_name='s3',
#        aws_access_key_id=access_key,
#        aws_secret_access_key=secret_key,
#        region_name = "us-west-1"
#)

#def setupUser


#ec2_resource = boto3.resource(
#                service_name='ec2',
#                region_name = 'us-west-1'
#)



#instance_profile = iam.InstanceProfile('attempt2')


#ec2_client.create_instances('try1')

#for instance in ec2_resource.instances.all():
#    print(instance.id)