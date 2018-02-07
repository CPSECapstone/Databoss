import boto3
import capture_cli

access_key = None
secret_key = None

#can be refactored to a function later
s3 = boto3.client(
        service_name='s3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='us-west-1'
    )
s3_resource = s3 = boto3.resource(
        service_name='s3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

def test_BucketCreation(bucketName):
    #create bucket
    capture.createBucket(bucketName)
    bucket_list = [bucket.name for bucket in s3.buckets.all()]
    for i in bucket_list:
        print("this is the bucket: ", i)
    assertTrue(bucketName in bucket_list)
    #assert that the bucket was created


#def test_BucketExists(bucketName):
    #create bucket

    #assert that the bucket was not created
test_BucketCreation('test2')