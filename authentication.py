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

# TODO: remove once hosted on ec2 instance
if os.path.exists("credentials.json"):
    credentialFile = open("credentials.json", "r")
    credentials = json.load(credentialFile)
    access_key = credentials['access']
    secret_key = credentials['secret']

#access key and secret key only needed for testing on local machine
ec2_resource = boto3.resource(
                service_name='ec2',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name = 'us-west-1'
)


#clientIam = boto3.client(service_name='iam')
#clientSts = boto3.client(service_name='sts')
#iam = boto3.resource('iam')

#tokenDuration = 86400 # duration in seconds
#region = 'us-west-1c'

#def loginUser(username, password):
#    session = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
#    credentials = session.get_credentials()
#    credentials = credentials.get_frozen_credentials()
   #access_key = credentials.access_key
   #secret_key = credentials.secret_key
#    return credentials

#this will attach the user's required iam instance profile (which should have the proper permissions) to an ec2 instance
#def login(imageId, ipName):
ec2_resource.create_instances(ImageId='ami-327f5352', #should be replaced with imageId
                     InstanceType='t2.micro',
                     MinCount=1, MaxCount=1,
                     IamInstanceProfile={
                            'Name': 'attempt3'
                     })