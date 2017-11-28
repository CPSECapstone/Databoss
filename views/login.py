from flask import Blueprint, request
import capture

login_api = Blueprint('login_api', __name__)


@login_api.route("/aws", methods=["POST"])
def login():
    print("logging in")
    data = request.json
    capture.access_key = data['access_key']
    capture.secret_key = data['secret_key']

    capture.aws_config()

    return "success"
