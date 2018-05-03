import sqlite3
import modelsQuery
from datetime import datetime



from flask import send_file
from web_app import app, db

import capture
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
    capture.aws_config()

    # TODO remove db additions here. for testing purposes only
    #db.drop_all()
    db.create_all()
'''


    modelsQuery.addReplay("Replay1", datetime(2018, 2, 5, 1, 1, 1), datetime(2018, 2, 5, 1, 1, 1), "myRDS2", 1, 1, "raw", "finished")
    modelsQuery.addReplay("Replay2", datetime(2018, 2, 5, 1, 1, 1), datetime(2018, 2, 5, 1, 1, 1), "myRDS2", 1, 1,
                          "raw", "active")

'''
if __name__ == "__main__":
    app.run('0.0.0.0')


