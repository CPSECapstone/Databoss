import models
import importlib

def testCreateTable():
    models.createTable()


def testAddGetMetric():
    n = 'metName'
    p = 'pathToMetric'
    models.addMetric(n, p)
    result = models.Metric.query.filter_by(name=n, path=p).all()
    assert result == 1
