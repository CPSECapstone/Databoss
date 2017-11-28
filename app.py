import sqlite3

from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy

import views.dbConnections

# Create the Flask application
app = Flask(__name__)

# Connect the MyCRT SQLite DB to the Flask app
sqlite = 'sqlite:///database.db'

app.config['SQLALCHEMY_DATABASE_URI'] = sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

app.register_blueprint(views.dbConnections.dbConnection_api, url_prefix="/db")

db = SQLAlchemy(app)

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