from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = None

# Connection format: dialect+driver://username:password@host:port/database
def addConnection(dialect, user, password, host, database):
    connection = dialect + "://" + user + ":" + password + "@" + host #+ "/" #\
                 # + database
    print(connection)
    app.config['SQLALCHEMY_DATABASE_URI'] = connection
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.debug = True
    global db
    db = SQLAlchemy(app)


if __name__ == "__main__":
    addConnection("mysql+pymysql", "master", "lolmpcsc480", "lolmp.cwaw8hrsce6c.us-west-1.rds.amazonaws.com:3306")
    print(db.session.execute("show databases;"))
