import boto3

user_key = input("Enter access key: ")
user_access = input("Enter secret key: ");

#s3 = boto3.client(
#    service_name='s3',
#    aws_access_key_id=user_key,
#    aws_secret_access_key=user_access,
    #region_name='us-west-1'
#)

s3_resource = boto3.resource(
   service_name = 's3',
    aws_access_key_id = user_key,
    aws_secret_access_key = user_access
)


bucket = s3_resource.Bucket('temp');
print(bucket.name);

#bucket2 = s3_resource.Bucket('temp2');
#print(bucket2.name);

#testing to see if I can print my bucket names out
for bucketInstance in s3_resource.buckets.all():
   print(bucket.name);

