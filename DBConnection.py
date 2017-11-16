from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = None

# Connection format: dialect+driver://username:password@host:port/database
def addConnection(dialect, user, password, host, database):
    connection = dialect + "://" + user + ":" + password + "@" + host + "/" \
                 + database
    print(connection)
    app.config['SQLALCHEMY_DATABASE_URI'] = connection
