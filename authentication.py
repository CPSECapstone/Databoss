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

clientIam = boto3.client(service_name='iam')
clientSts = boto3.client(service_name='sts')
iam = boto3.resource('iam')

tokenDuration = 86400 # duration in seconds
accessKey = '' # Place access key
secretKey = '' # Place secret key
region = 'us-west-1'

def loginUser(username, password):
    session = boto3.Session(aws_access_key_id=accessKey, aws_secret_access_key=secretKey, region_name=region)
    credentials = session.get_credentials()
    credentials = credentials.get_frozen_credentials()
    #access_key = credentials.access_key
    #secret_key = credentials.secret_key
    return credentials