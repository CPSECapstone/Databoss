from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, exc
import modelsQuery

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
    dbConns = modelsQuery.getDBConnectionAll()
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
        modelsQuery.addDBConnection(dialect, name, user, host, port, database)
    except exc.OperationalError:
        print("Unable to connect")

    modelsQuery.addDBConnection(dialect, name, user, host, port, database)

    dbc = modelsQuery.getDBConnectionAll()
    print(dbc)
