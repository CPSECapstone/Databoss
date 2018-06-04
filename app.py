import sqlite3
import modelsQuery
from datetime import datetime

from flask import send_file
from web_app import app, db, socketio
from flask_socketio import disconnect, join_room, leave_room, close_room
import atexit, os
import models

import capture
from views import dbConnection, login, metrics, replay, capture as cap

thread = None

app.register_blueprint(dbConnection.dbc_api, url_prefix="/dbc")
app.register_blueprint(capture.capture_api, url_prefix="/capture")
app.register_blueprint(login.login_api, url_prefix="/login")
app.register_blueprint(metrics.metrics_api, url_prefix="/metrics")
app.register_blueprint(replay.replay_api, url_prefix="/replay")

@app.route('/')
def main():
    return send_file('static/app/index.html')


@app.before_first_request
def sqlite_setup():
    print("Running sqlite.py setup")
    conn = sqlite3.connect('database.db')
    conn.close()
    capture.aws_config()

    # TODO remove db additions here. for testing purposes only
    #db.drop_all()
    db.create_all()
'''

    modelsQuery.addReplay("Replay1", datetime(2018, 2, 5, 1, 1, 1), datetime(2018, 2, 5, 1, 1, 1), "myRDS2", 1, 1, "raw", "finished")
    modelsQuery.addReplay("Replay2", datetime(2018, 2, 5, 1, 1, 1), datetime(2018, 2, 5, 1, 1, 1), "myRDS2", 1, 1,
                          "raw", "active")

'''
@socketio.on('connect', namespace='')
def test_connect():
    print("socketio connected")


@socketio.on('disconnect_request', namespace='')
def disconnect_request():
    print("socketio disconnect")
    disconnect()


@socketio.on('join', namespace='')
def join(message):
    from replay import getInProgressReplay

    join_room(message['room'])
    current_replay = getInProgressReplay(message['room'])

    if current_replay:
        current_replay['connected'] = True
        print("User has connected to room", message['room'])


@socketio.on('leave', namespace='')
def leave(message):
    leave_room(message['room'])


@socketio.on('close_room', namespace='')
def close(message):
    close_room(message['room'])


# Set captures and replays that are in progress to failed when system exits
def exit_handler():
    inProgressCaptures = models.Capture.query.filter((models.Capture.status == "active") | (models.Capture.status == "scheduled")).all()
    inProgressReplays = models.Replay.query.filter((models.Replay.status == "active")).all()

    for failedCap in inProgressCaptures:
        failedCap.status = "failed"

    for failedRep in inProgressReplays:
        failedRep.status = "failed"

    models.db.session.commit()

    # Remove replay temp files
    directory = os.listdir(".")
    for item in directory:
        if item.endswith("tempLogFile"):
            print(item)
            os.remove(item)


atexit.register(exit_handler)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True, port=5000)
