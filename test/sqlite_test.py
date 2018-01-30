import sqlite
import importlib

def testCreateTable():
    sqlite.createTable()
    assert sqlite.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metric'").fetchone()
    assert sqlite.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dbConnection'").fetchone()
    assert sqlite.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workload'").fetchone()
    assert sqlite.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logfile'").fetchone()
    assert sqlite.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='capture'").fetchone()
    assert sqlite.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='replay'").fetchone()

def testAddMetric():
    sqlite.addMetric('test', 'path')