from flask_sqlalchemy import SQLAlchemy
from app import app, db
import sqlalchemy
import models


# Connection format: dialect+driver://username:password@host:port/database
def add_connection(dialect, name, user, password, host, port, database):
    connection = dialect + "://" + user + ":" + password + "@" + host + ":"\
                 + port + "/" + database
    print(connection)

    # Test that the connection is valid/authorized
    # If so, add the connection to the MyCRT SQLite db
    try:
        sqlalchemy_binds = {
            'capture': connection
        }

        app.config['SQLALCHEMY_BINDS'] = sqlalchemy_binds

        capture_db = SQLAlchemy(app)
        capture_db.engine.connect()

        __add_to_mycrt_db(dialect, name, user, host, port, database)

        dbc = models.DBConnection.query.all()
        print(dbc)

    # Catch errors when trying to connect with the db information
    except sqlalchemy.exc.OperationalError:
        print("Unable to connect")

# Add a new DBConnection to the MyCRT SQLite database
def __add_to_mycrt_db(dialect, name, user, host, port, database):
    new_db = models.DBConnection(dialect=dialect, name=name, host=host,
                                 port=port, database=database, username=user)

    db.session.add(new_db)
    db.session.commit()


if __name__ == "__main__":
    password = input('Enter your password: ')
    db.create_all()
    add_connection("mysql+pymysql", "test", "master", password, "lolmp.cwaw8hrsce6c.us-west-1.rds.amazonaws.com", "3306",
                   "lolmp")
