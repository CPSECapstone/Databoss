from flask_sqlalchemy import SQLAlchemy
from app import app, db
import sqlalchemy


# Connection format: dialect+driver://username:password@host:port/database
def add_connection(dialect, user, password, host, database):
    connection = dialect + "://" + user + ":" + password + "@" + host #+ "/" + database
    print(connection)

    try:
        sqlalchemy_binds = {
            'capture': 'mysqldb://localhost/users'
        }

        app.config['SQLALCHEMY_BINDS'] = sqlalchemy_binds

        capture_db = SQLAlchemy(app)
        capture_db.engine.connect()
    except sqlalchemy.exc.OperationalError:
        print("Unable to connect")


def __add_to_mycrt_db(dialect, user, password, host, database):
    return 1


if __name__ == "__main__":
    password = input('Enter your password: ')
    add_connection("mysql+pymysql", "master", password, "lolmp.cwaw8hrsce6c.us-west-1.rds.amazonaws.com:3306",
                   "lolmp")
