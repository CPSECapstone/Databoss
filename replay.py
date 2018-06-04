import boto3
import pymysql
import botocore
import sys
import capture
import logging
from datetime import datetime
import modelsQuery
from ast import literal_eval
from threading import Timer
import time
import json
import os.path
import sys
from web_app import socketio
import flask_socketio


logger = logging.getLogger()
logger.setLevel(logging.INFO)


inProgressReplays = []


def addInProgressReplay(replayName, username, password):
    inProgressReplays.append({'replayName': replayName, 'username': username, 'password': password, 'connected': False})


def getInProgressReplay(replayName):
    for replay in inProgressReplays:
        if replay.get('replayName') == replayName:
            return replay

    return None


def removeInProgressReplay(replayName):
    for replay in inProgressReplays:
        if replay.get('replayName') == replayName:
            inProgressReplays.remove(replay)


def download_file(replayName, bucketName, fileName):
    try:
        capture.s3.Bucket(bucketName).download_file(fileName, replayName + " " + "tempLogFile")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The file does not exist.")
        else:
            raise

def executeTimePreserving(queryTable, replayName, captureName, dbName, status_of_db, totalQueries, endpoint, username, password, start_time, lastTime):
    metricBucket = modelsQuery.getCaptureMetricBucket(captureName)
    #totalQueries = 0
    numQueriesExecuted = 0
    numQueriesFailed = 0

    # wait for client to connect for first time before executing
    while not checkUserConnected(replayName):
        pass

    print("Replay detects user has connected and will now start replaying")

    try:
        conn = pymysql.connect(host=endpoint, user=username, passwd=password, connect_timeout=5)
    except:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
        # conn.close()
        sys.exit()

    count = 0
    print("~~~~~~~ starting time preserving replay ~~~~~~")

    for i in queryTable:
        time.sleep(i['timeDiff'])
        executableQuery = i['Query']
        print(executableQuery)
        if str(status_of_db) == "available":
            with conn.cursor() as cur:
                status = 'Success'
                error = ''
                try:
                    cur.execute(executableQuery)
                    numQueriesExecuted += 1
                    print("num execute: ", numQueriesExecuted)

                except pymysql.err.Error as err:
                    error = err

                if error:
                    status = 'Fail'
                    numQueriesFailed += 1
                    error = str(error).replace('(', '').replace(')', '').strip()

                count += 1
                emitLiveQuery(replayName, executableQuery, status, error, count)

    if (lastTime != 0):
        time.sleep(lastTime)

    print("~~~~~~ finished time preserving replay ~~~~~~")
    endTime = datetime.now()
    modelsQuery.updateReplayStatus(replayName, "finished")
    modelsQuery.updateReplayQueries(replayName, totalQueries, numQueriesExecuted, numQueriesFailed)
    modelsQuery.updateReplayEndTime(replayName, endTime)
    metricID = modelsQuery.getMetricIDByNameAndBucket(replayName + " " + "metric file", metricBucket)
    capture.sendMetrics(metricID, replayName + " " + "metric file", start_time, endTime)



def calculateTimeDiff(queryTable):
    timeDictionary = {'timeDiff': 0}
    queryTable[0].update(timeDictionary)
    queryTableLen = len(queryTable)
    print(queryTableLen)

    for queryTableIndx in range(1, queryTableLen):
        timeDictionary = {
            'timeDiff': queryTable[queryTableIndx]['timestamp'] - queryTable[queryTableIndx - 1]['timestamp']}
        queryTable[queryTableIndx].update(timeDictionary)


def setupQueryTable(temp, queryTable):
        flag = False
        for line in temp:
            entireDict = literal_eval(line)
            dictLength = len(entireDict)
            #totalQueries = len(entireDict)
            print(dictLength)
            for indx in range(dictLength):
                tempDict = dict()
                val = entireDict[indx]
                print(val)

                if val['message'].startswith('Query'):
                    tempDict['timestamp'] = val['timestamp']
                    tempDict['Query'] = val['message'][7:]
                    queryTable.append(tempDict)
            if len(queryTable) == 0:
                flag = True
                print("comes in this if")
                break
        return flag

def calculateLastTime(queryTable, captureLength):
    start = queryTable[0]['timestamp']
    end = queryTable[len(queryTable)-1]['timestamp']
    entireQueryTime = end - start
    lastTimeDiff = captureLength.total_seconds() - entireQueryTime
    return lastTimeDiff

def timePreserving(capLength, replayName, captureObj, dbName, mode, endpoint, status_of_db, username, password):
    flag = False
    queryTable = []
    captureName = captureObj['name']

    with open(captureName + " " + "tempLogFile", "r") as temp:
        try:
            conn = pymysql.connect(host=endpoint, user=username, passwd=password, connect_timeout=5)
        except:
            logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
            if os.path.exists(captureName + " " + "tempLogFile"):
                os.remove(captureName + " " + "tempLogFile")
            # conn.close()
            sys.exit()

        flag = setupQueryTable(temp, queryTable)
        totalQueries = len(queryTable)

        if (flag == False):
            #calculating time diff from all queries
            calculateTimeDiff(queryTable)
            #function that adds up all the times and gets the diff between last query ran and entire cap length
            lastTime = calculateLastTime(queryTable, capLength)

            t3 = Timer(0, executeTimePreserving, [queryTable, replayName, captureName, dbName, status_of_db, totalQueries, endpoint, username, password, datetime.now(), lastTime])
            t3.start()
        else:
            endTime = datetime.now()
            modelsQuery.updateReplayStatus(replayName, "finished")
            modelsQuery.updateReplayQueries(replayName, 0, 0, 0)
            modelsQuery.updateReplayEndTime(replayName, endTime)


def startReplay(replayName, captureObj, rdsInstance, mode, username, password):
    captureObj = json.loads(captureObj)
    captureName = captureObj['name']
    print("name: " + captureName)
    logfile = modelsQuery.getLogFileByCapture(captureName)
    dbName = rdsInstance
    endpoint = capture.get_list_of_instances(rdsInstance)['DBInstances'][0]['Endpoint']['Address']
    status_of_db = capture.get_list_of_instances(rdsInstance)['DBInstances'][0]['DBInstanceStatus']

    metricFileName = replayName + " " + "metric file"

    captureStartTime = modelsQuery.getCaptureStartTime(captureName)
    captureEndTime = modelsQuery.getCaptureEndTime(captureName)
    metricFile = modelsQuery.getCaptureMetric(captureName)
    captureID = modelsQuery.getCaptureID(captureName)
    captureBucket = modelsQuery.getCaptureBucket(captureName)
    metricBucket = modelsQuery.getMetricBucketByName(captureName)
    filename = logfile.filename

    #adding replay metrics to the bucket.
    modelsQuery.addMetric(metricFileName, metricBucket, None)
    metricID = modelsQuery.getMetricIDByNameAndBucket(metricFileName, metricBucket)


    ## how to get the current time of the system.
    replayStartTime = datetime.now()
    print("Capture start time: " + captureStartTime.strftime('%m/%d/%Y :%H:%M'))
    print("Current system time: " + replayStartTime.strftime('%m/%d/%Y% :H:%M'))

    download_file(captureName, captureBucket, filename)

    modelsQuery.addDBConnection('mysql', rdsInstance, endpoint, 3306, dbName, username)
    addInProgressReplay(replayName, username, password)

    if mode == 'time-preserving':
        timeDifference = captureEndTime - captureStartTime
        print('timeDiff in capture: ')
        print(timeDifference)
        modelsQuery.addReplay(replayName, replayStartTime, None, dbName, metricID, captureID, mode, "active")
        timePreserving(timeDifference, replayName, captureObj, dbName, mode, endpoint, status_of_db, username, password)
    else:
        modelsQuery.addReplay(replayName, replayStartTime, None, dbName, metricID, captureID, mode, "active")
        t2 = Timer(0, executeReplay, [replayName, captureName, dbName, status_of_db, endpoint, datetime.now()])
        t2.start()

def executeReplay(replayName, captureName, dbName, status_of_db, endpoint, startTime):
    print("capture name here: " + captureName)
    print("db name: " + dbName)
    metricBucket = modelsQuery.getCaptureMetricBucket(captureName)
    inProgressReplay = getInProgressReplay(replayName)
    username = inProgressReplay.get('username')
    password = inProgressReplay.get('password')

    totalQueries = 0
    numQueriesExecuted = 0
    numQueriesFailed = 0

    # wait for client to connect for first time before executing
    while not checkUserConnected(replayName):
        pass

    print("Replay detects user has connected and will now start replaying")

    with open(captureName + " " + "tempLogFile", 'r') as tempFile:
        try:
            conn = pymysql.connect(host=endpoint, user=username, passwd=password, connect_timeout=5)
        except:
            logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
            if os.path.exists(captureName + " " + "tempLogFile"):
                os.remove(captureName + " " + "tempLogFile")
            # conn.close()
            sys.exit()

        count = 0
        print("~~~~~~~ starting raw replay ~~~~~~")
        for line in tempFile:
            entireList = literal_eval(line)
            queryList = [entry for entry in entireList if entry['message'].startswith('Query')]
            totalQueries = len(queryList)

            for i in range(totalQueries):
                dict = queryList[i]
                if dict['message'].startswith('Query'):
                    executableQuery = dict['message'][7:]
                    if str(status_of_db) == "available":
                        with conn.cursor() as cur:
                            # socketio.sleep(0.5)
                            status = 'Success'
                            error = ''
                            try:
                                print(executableQuery)
                                cur.execute(executableQuery)
                                numQueriesExecuted += 1

                            except pymysql.err.Error as err:
                                error = err

                            if error:
                                status = 'Fail'
                                numQueriesFailed += 1
                                error = str(error).replace('(', '').replace(')', '').strip()

                            count += 1
                            emitLiveQuery(replayName, executableQuery, status, error, count)

    print("~~~~~~ finished replay ~~~~~~")

    if os.path.exists(captureName + " " + "tempLogFile"):
        os.remove(captureName + " " + "tempLogFile")

    endTime = datetime.now()
    modelsQuery.updateReplayStatus(replayName, "finished")
    modelsQuery.updateReplayQueries(replayName, totalQueries, numQueriesExecuted, numQueriesFailed)
    modelsQuery.updateReplayEndTime(replayName, endTime)
    metricID = modelsQuery.getMetricIDByNameAndBucket(replayName + " " + "metric file", metricBucket)
    capture.sendMetrics(metricID, replayName + " " + "metric file", startTime, endTime)

    conn.close()


def emitLiveQuery(room, executableQuery, status, error, count):
    socketio.emit('replayQuery',
                  {'query': executableQuery.lower(), 'status': status, 'error': error, 'count': count},
                  namespace='', room=room)


def checkUserConnected(replayName):
    replay = getInProgressReplay(replayName)
    return replay.get('connected')