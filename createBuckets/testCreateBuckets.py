import boto3

user_key = input("Enter access key: ")
user_access = input("Enter secret key: ");

client = boto3.client('s3',
    aws_access_key_id=user_key,
    aws_secret_access_key=user_access
#    region_name='us-west-2'
)


#using AWS s3
s3 = boto3.resource('s3');

#testing to see if I can print my bucket names out
for bucket in s3.buckets.all():
    print(bucket.name);
#response = s3.list_buckets();
#s3.create_bucket(Bucket ='Log Files');