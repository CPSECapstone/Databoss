import sqlite3


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

    #db.drop_all()
    db.create_all()
    

if __name__ == "__main__":
    app.run(debug=True)