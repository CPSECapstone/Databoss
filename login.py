import boto3
import time
import pymysql
import botocore
import random
import sys
import string
import logging
from flask import Blueprint, jsonify


iam = boto3.client('iam')
user_name = 'demo_1'

try:
    response = iam.get_login_profile(UserName=user_name)
except Exception as e:
        print('User {} has no login profile'.format(user_name))