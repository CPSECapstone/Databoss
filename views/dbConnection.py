from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, exc
from web_app import db
import models

dbc_api = Blueprint('dbc_api', __name__)


# Connection format: dialect+driver://username:password@host:port/database
@dbc_api.route("/add", methods=["POST"])
def add():
    print("trying to add connection")
    data = request.json

    dialect = "mysql+pymysql"
    name = data['name']
    username = data['username']
    password = data['password']
    host = data['host']
    port = data['port']
    database = data['database']

    __add_connection(dialect, name, username, password, host, port, database)

    return "success"


@dbc_api.route("/get", methods=["GET"])
def get():
    dbConns = models.DBConnection.query.all()
    return jsonify([i.serialize for i in dbConns])


def __add_connection(dialect, name, user, password, host, port, database):
    connection = dialect + "://" + user + ":" + password + "@" + host + ":"\
                 + port + "/" + database
    print(connection)

    # Test that the connection is valid/authorized
    # If so, add the connection to the MyCRT SQLite db
    try:
        engine = create_engine(connection)
        engine.connect()
        __add_to_mycrt_db(dialect, name, user, host, port, database)
    except exc.OperationalError:
        print("Unable to connect")

    __add_to_mycrt_db(dialect, name, user, host, port, database)

    dbc = models.DBConnection.query.all()
    print(dbc)


# Add a new DBConnection to the MyCRT SQLite database
def __add_to_mycrt_db(dialect, name, user, host, port, database):
    new_db = models.DBConnection(dialect=dialect, name=name, host=host,
                                 port=port, database=database, username=user)

    db.session.add(new_db)
    db.session.commit()
