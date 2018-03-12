from flask import Blueprint, request, jsonify, Response
import capture
import boto3
import botocore
import json
from boto3 import Session

login_api = Blueprint('login_api', __name__)


@login_api.route("/aws", methods=["POST"])
def login():
    capture.aws_config()
    return "success"
