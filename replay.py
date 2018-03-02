import boto3
import time
import pymysql
import botocore
import random
import sys
import string
import logging
from flask import Blueprint, jsonify
from datetime import timedelta
from datetime import datetime
from time import mktime
import rds_config
import modelsQuery

def startReplay(replayName, captureBucket, dbName, startDate, endDate, startTime, endTime, storage_limit, mode):
    print("start replay")
    #get log file that corresponds to the capture
    #connect to database dbName
    #execute queries in file
    #get metrics from cloudwatch
    #update database for a replay
    #modelsQuery.addReplay(replayName, )
