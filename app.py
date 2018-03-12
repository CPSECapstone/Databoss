import sqlite3
#import rds_config

from flask import send_file
from web_app import app, db
from datetime import datetime

import capture
import modelsQuery
from views import dbConnection, login, metrics, replay, capture as cap

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

    # TODO remove db additions here. for testing purposes only

    db.drop_all()
    db.create_all()

    modelsQuery.addCapture("Capture1", datetime(2018, 2, 5, 1, 0, 0), datetime(2018, 2, 5, 5, 0, 0), "myRDS1", 1, 1, "interactive", "finished")
    modelsQuery.addReplay("Replay1", datetime(2018, 2, 5, 1, 1, 1), datetime(2018, 2, 5, 1, 1, 1), "myRDS2", 1, 1, "raw", "finished")
    modelsQuery.addReplay("Replay2", datetime(2018, 2, 5, 1, 1, 1), datetime(2018, 2, 5, 1, 1, 1), "myRDS3", 2, 2, "raw", "finished")

    modelsQuery.addCapture("Capture2", datetime(2018, 2, 5, 2, 30, 15), datetime(2018, 2, 5, 4, 30, 1), "myRDS4", 2, 2, "interactive", "finished")
    modelsQuery.addReplay("Replay3", datetime(2018, 2, 5, 1, 1, 1), datetime(2018, 2, 5, 1, 1, 1), "myRDS5", 3, 3, "raw", "finished")
    modelsQuery.addReplay("Replay4", datetime(2018, 2, 5, 1, 1, 1), datetime(2018, 2, 5, 1, 1, 1), "myRDS6", 4, 4, "raw", "finished")

    modelsQuery.addCapture("Capture3", datetime(2018, 2, 5, 2, 30, 15), datetime(2018, 2, 5, 4, 30, 1), "myRDS4", 2, 2,
                           "interactive", "finished")
    modelsQuery.addCapture("Capture4", datetime(2018, 2, 5, 2, 30, 15), datetime(2018, 2, 5, 4, 30, 1), "myRDS4", 2, 2,
                           "interactive", "finished")
    modelsQuery.addCapture("Capture5", datetime(2018, 2, 5, 2, 30, 15), datetime(2018, 2, 5, 4, 30, 1), "myRDS4", 2, 2,
                           "interactive", "finished")
    modelsQuery.addMetric("Metrics1", "crt-metrics-test", "metric-file.txt")
    modelsQuery.addMetric("Metrics2", "crt-metrics-test", "metric-file-2.txt")
    modelsQuery.addLogfile("Logfile1", "my-bucket", "my-file")


if __name__ == "__main__":
    app.run(debug=False)
