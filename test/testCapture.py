import boto3
import capture
import testStorage
import pytest
import json
import os.path

access_key = None
secret_key = None


if os.path.exists("../credentials.json"):
    credentialFile = open("../credentials.json", "r")
    credentials = json.load(credentialFile)
    access_key = credentials['access']
    secret_key = credentials['secret']
    capture.aws_config(access_key, secret_key)
    testStorage.aws_config(access_key, secret_key)
else:
    print("ERROR: could not find credentials")

s3 = boto3.client(
        service_name='s3'
    )
s3_resource = s3 = boto3.resource(
        service_name='s3'
    )

def test_BucketCreation(bucketName):
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    initialSize = bucket_list.__len__()
    capture.createBucket(bucketName)
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    sizeAfterAdd = bucket_list.__len__()
    assert len(bucket_list) == sizeAfterAdd

def test_BucketExists(bucketName):
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    initialSize = bucket_list.__len__()
    capture.createBucketName(bucketName, bucketName)
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    sizeAfterAdd = bucket_list.__len__()
    assert (initialSize == sizeAfterAdd)

def test_StorageMax(size, db_name):
    testStorage.startRDS(db_name, "sthanawa", "sthanawa", "storagedb.coircswctb4r.us-west-1.rds.amazonaws.com")
    res = testStorage.checkStorageCacity(size, db_name)
    assert (res == -1)

def test_Storage(size, db_name):
    testStorage.startRDS(db_name, "sthanawa", "sthanawa", "storagedb.coircswctb4r.us-west-1.rds.amazonaws.com")
    res = testStorage.checkStorageCacity(size, db_name)
    assert (res == 0)

test_BucketCreation('capture-test-6')
test_BucketExists('capture-test-6')
#test_StorageMax(5, 'storagedb')
#test_Storage(25, 'storagedb')
