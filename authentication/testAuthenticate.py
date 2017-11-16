import boto3

user_key = input("Enter user key id: ")
user_access = input("Enter user access id: ");

client = boto3.client(
    service_name='rds',
    aws_access_key_id=user_key,
    aws_secret_access_key=user_access,
    region_name='us-west-2'

)

print(client.describe_db_instances())

