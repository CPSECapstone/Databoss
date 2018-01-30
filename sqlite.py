import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Sets up the tables in the database and their connections. Should be called only once.
def createTable():
    # Metric
    c.execute('''CREATE TABLE metric
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  path TEXT UNIQUE)''')
    # DBConnection
    c.execute('''CREATE TABLE dbConnection
                 (id INTEGER PRIMARY KEY,
                  hostname TEXT,
                  port INTEGER,
                  user TEXT)''')
    # Workload
    c.execute('''CREATE TABLE workload
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  path TEXT UNIQUE)''')
    # Logfile
    c.execute('''CREATE TABLE logfile
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  path TEXT UNIQUE)''')
    # Capture
    c.execute('''CREATE TABLE capture
                 (id INTEGER PRIMARY KEY,
                  FOREIGN KEY (dbId) REFERENCES dbConnection(id),
                  FOREIGN KEY (logfileId) REFERENCES logfile(id),
                  FOREIGN KEY (workloadId) REFERENCES workload(id),
                  FOREIGN KEY (metricId) REFERENCES metric(id))''')
    # Replay
    c.execute('''CREATE TABLE replay
                 (id INTEGER PRIMARY KEY,
                  FOREIGN KEY (dbId) REFERENCES dbConnection(id),
                  FOREIGN KEY (logfileId) REFERENCES logfile(id),
                  FOREIGN KEY (workloadId) REFERENCES workload(id),
                  FOREIGN KEY (metricId) REFERENCES metric(id),
                  FOREIGN KEY (captureId) REFERENCES capture(id))''')

    c.commit()


# Variable = (value,) is used to protect database from SQL Injection Attacks

# Add metric information to the metric table
def addMetric(metricName, path):
    metric = (metricName, path)
    c.execute("INSERT INTO metric(name, path) VALUES (?, ?)", metric)

    c.commit()

# Retrieve metric path by referencing metric name
def getMetricPath(metricName):
    m = (metricName,)
    c.execute("SELECT path FROM metric WHERE name=?", m)
    row = c.fetchone()
    return row[0]

# Close the connection to the DB SQLite
def closeConn():
    conn.close()