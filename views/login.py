from flask import Blueprint, request, jsonify, Response
import capture
import boto3
import botocore
import json
from boto3 import Session

login_api = Blueprint('login_api', __name__)


@login_api.route("/aws", methods=["POST"])
def login():
    print("logging in")
    data = request.json
    imageId = data['ec2-ami']
    iamRole = data['iamRole']

    ec2_resource = boto3.resource(
        service_name='ec2',
        region_name='us-west-1'
    )

    try:
        ec2_resource.create_instances(ImageId=imageId,
                                  InstanceType='t2.micro',
                                  MinCount=1, MaxCount=1,
                                  IamInstanceProfile={
                                      'Name': iamRole
                                  })
    except Exception as e:
        return Response('Failed to start up ec2 instance - check image id and iam role', status=500)

    return "success"
