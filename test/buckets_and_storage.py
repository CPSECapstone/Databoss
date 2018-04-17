import boto3
import capture
import scheduler
from datetime import datetime

def test_BucketCreation():
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

    bucketName = 'capture-test-5'

    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    capture.createBucket(bucketName)
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    sizeAfterAdd = bucket_list.__len__()
    assert len(bucket_list) == sizeAfterAdd



def test_BucketExists():
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

    bucketName = 'capture-test-5'
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    initialSize = bucket_list.__len__()
    capture.createBucketName(bucketName, bucketName)
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    sizeAfterAdd = bucket_list.__len__()
    assert (initialSize == sizeAfterAdd)


def test_StorageScheduled():
    size = 25
    db_name = 'storage_db'
    db_username = 'sthanawa'
    db_password = 'sthanawa'
    db_endpoint = 'storagedb.coircswctb4r.us-west-1.rds.amazonaws.com'
    capture.startRDS(db_name, db_username, db_password, db_endpoint)
    #this will be false first because the scheduled storage shouldn't be set first
    initialStorage = scheduler.storageResult
    scheduler.scheduleStorageCapture(datetime.now(), 5, 20, "test1")
    #this will be true after scheduled storage is met
    res = scheduler.storageResult

    assert (initialStorage != res)
