import boto3
import capture
import testStorage
import pytest
import json
import os.path


loc = "us-west-1"
s3 = boto3.client(
        service_name='s3'
    )
s3_resource = s3 = boto3.resource(
        service_name='s3'
    )

rds = boto3.client(
        service_name='rds',
        region_name=loc
    )

bucketName = 'capture-test-13'
# def pytest_namespace():
#     return {'bucketName': 'capture-test-6'}
#
# @pytest.fixture
# def data():
#     pytest.bucketName = 'capture-test-6'
#
# @pytest.fixture
# def initializeBoto():
#     s3 = boto3.client(
#         service_name='s3'
#     )
#     s3_resource = s3 = boto3.resource(
#         service_name='s3'
#     )


def test_BucketCreation():
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    capture.createBucket(bucketName)
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    sizeAfterAdd = bucket_list.__len__()
    assert len(bucket_list) == sizeAfterAdd



def test_BucketExists():
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    initialSize = bucket_list.__len__()
    capture.createBucketName(bucketName, bucketName)
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    sizeAfterAdd = bucket_list.__len__()
    assert (initialSize == sizeAfterAdd)

# def test_StorageMax():
#     size = 5
#     db_name = 'testing'
#     testStorage.startRDS(db_name, "master", "password", "testing.ckunormkfqio.us-west-1.rds.amazonaws.com")
#     res = testStorage.checkStorageCacity(size, db_name)
#     assert (res == -1)

# def test_Storage(size, db_name):
#     testStorage.startRDS(db_name, "sthanawa", "sthanawa", "storagedb.coircswctb4r.us-west-1.rds.amazonaws.com")
#     res = testStorage.checkStorageCacity(size, db_name)
#     assert (res == 0)
#
# test_BucketCreation('capture-test-6')
# test_BucketExists('capture-test-6')
# #test_StorageMax(5, 'storagedb')
# #test_Storage(25, 'storagedb')
