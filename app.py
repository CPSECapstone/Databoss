import sqlite3

from flask import Flask, send_file
from web_app import app, db

import views.dbConnection
import capture
import views.login

app.register_blueprint(views.dbConnection.dbc_api, url_prefix="/dbc")
app.register_blueprint(capture.capture_api, url_prefix="/capture")
app.register_blueprint(views.login.login_api, url_prefix="/login")


@app.route('/')
def main():
    return send_file('static/app/index.html')


@app.before_first_request
def sqlite_setup():
    print("Running sqlite setup")
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute(
        'CREATE TABLE if not exists users (name TEXT, dbName TEXT, logInfo TEXT, metricInfo TEXT)')

    print("Table created successfully")
    conn.close()

    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)