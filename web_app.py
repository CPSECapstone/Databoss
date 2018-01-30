from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the Flask application
app = Flask(__name__)

# Connect the MyCRT SQLite DB to the Flask app
sqlite = 'sqlite.py:///database.db'

app.config['SQLALCHEMY_DATABASE_URI'] = sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

db = SQLAlchemy(app)
