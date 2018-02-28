import boto3

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