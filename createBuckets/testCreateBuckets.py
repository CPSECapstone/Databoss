import boto3

def getLocation(num):
    if num == "1":
        return "us-west-1";
    elif num == "2":
        return "us-west-2";
    elif num == "3":
        return "eu-west-1";
    elif num == "4":
        return "eu-west-2";
    elif num == "5":
        return "eu-central-1";
    elif num == "6":
        return "ap-south-1";
    elif num == "7":
        return "ap-southeast-1";
    elif num == "8":
        return "ap-southeast-2";
    elif num == "9":
        return "ap=northeast-1";
    elif num == "10":
        return "ap-northeast-2";
    elif num == "11":
        return "sa-east-1";
    elif num == "12":
        return " "; #if US East then input for login constraints needs to be an empty string
    elif num == "13":
        return "us-east-2";
    else:
        return "ERROR";


user_key = input("Enter access key: ")
user_access = input("Enter secret key: ");

#Don't think client is necessary
#s3 = boto3.client(
#    service_name='s3',
#    aws_access_key_id=user_key,
#    aws_secret_access_key=user_access,
    #region_name='us-west-1'
#)

s3_resource = boto3.resource(
    service_name = 's3',
    aws_access_key_id = user_key,
    aws_secret_access_key = user_access,

)

#I think user should be able to indicate location of bucket. If so then we can use this next line:
log_location_num = input("""
Where should bucket for log files be located?\n 1 - us-west-1\n 2 - us-west-2\n 3 - eu-west-1
 4 - eu-west-2\n 5 - eu-central-1\n 6 - ap-south-1\n 7 - ap-southeast-1\n 8 - ap-southeast-2\n 9 - ap-northeast-1
 10 - ap-northeast-2\n 11 - sa-east-1\n 12 - US East (N. Virginia) region\n 13 - us-east-2\n
""");


log_location = getLocation(log_location_num);
if (log_location != "ERROR"):
    s3_resource.create_bucket(Bucket='saloneetest',
                              CreateBucketConfiguration={
                            'LocationConstraint': log_location});
else:
    print("Not a possible location\n");

#bucket = s3_resource.Bucket('temp');
#print(bucket.name);

#bucket2 = s3_resource.Bucket('temp2');
#print(bucket2.name);

#testing to see if I can print my bucket names out
#for bucketInstance in s3_resource.buckets.all():
#   print(bucketInstance.name);

