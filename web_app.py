from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from threading import Lock
from flask import Flask
from flask_socketio import SocketIO, emit

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

# Create the Flask application
app = Flask(__name__)

# Connect the MyCRT SQLite DB to the Flask app
sqlite = 'sqlite:///database.db'

app.config['SQLALCHEMY_DATABASE_URI'] = sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

db = SQLAlchemy(app)

socketio = SocketIO(app, async_mode=async_mode)
thread_lock = Lock()
