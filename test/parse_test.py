import parseMetrics
import pytest

@pytest.fixture
def jsonString():
    return '[{"Label": "CPUUtilization", "Datapoints": [{"Timestamp": 1516335600, "Average": 2.19147911456887, ' \
           '"Unit": "Percent"}, {"Timestamp": 1516334100, "Average": 2.468315272760944, "Unit": "Percent"}, ' \
           '{"Timestamp": 1516336200, "Average": 2.433574140965086, "Unit": "Percent"}, {"Timestamp": 1516337100, ' \
           '"Average": 2.259887005649732, "Unit": "Percent"}, {"Timestamp": 1516334400, "Average": 2.566379549874962, ' \
           '"Unit": "Percent"}, {"Timestamp": 1516335000, "Average": 2.35871075298693, "Unit": "Percent"}, ' \
           '{"Timestamp": 1516335900, "Average": 2.333592664629064, "Unit": "Percent"}, {"Timestamp": 1516336500, ' \
           '"Average": 2.2008057793831517, "Unit": "Percent"}, {"Timestamp": 1516333800, "Average": ' \
           '2.440677966101698, "Unit": "Percent"}, {"Timestamp": 1516334700, "Average": 2.36607390941929, ' \
           '"Unit": "Percent"}, {"Timestamp": 1516336800, "Average": 2.2341576363804743, "Unit": "Percent"}, ' \
           '{"Timestamp": 1516335300, "Average": 2.2745762711864463, "Unit": "Percent"}], "ResponseMetadata": {' \
           '"RequestId": "3f419773-fc91-11e7-9a68-091e021bc9b8", "HTTPStatusCode": 200, "HTTPHeaders": {' \
           '"x-amzn-requestid": "3f419773-fc91-11e7-9a68-091e021bc9b8", "content-type": "text/xml", "content-length": ' \
           '"2238", "vary": "Accept-Encoding", "date": "Thu, 18 Jan 2018 20:50:41 GMT"}, "RetryAttempts": 0}}, ' \
           '{"Label": "ReadIOPS", "Datapoints": [{"Timestamp": 1516337100, "Average": 0.23336444859314573, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516334400, "Average": 0.33999999999999997, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516335000, "Average": 0.23334111137037902, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516335900, "Average": 0.23333333333333334, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516336500, "Average": 0.23330611428666653, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516333800, "Average": 0.2366546117397804, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516334700, "Average": 0.2333294445092582, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516336800, "Average": 0.23334500058336252, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516335300, "Average": 0.23335666900023339, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516335600, "Average": 0.23333333333333334, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516334100, "Average": 0.2333294445092582, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516336200, "Average": 0.2366355597031507, ' \
           '"Unit": "Count/Second"}], "ResponseMetadata": {"RequestId": "3f48ea82-fc91-11e7-9a68-091e021bc9b8", ' \
           '"HTTPStatusCode": 200, "HTTPHeaders": {"x-amzn-requestid": "3f48ea82-fc91-11e7-9a68-091e021bc9b8", ' \
           '"content-type": "text/xml", "content-length": "2312", "vary": "Accept-Encoding", "date": "Thu, ' \
           '18 Jan 2018 20:50:41 GMT"}, "RetryAttempts": 0}}, {"Label": "WriteIOPS", "Datapoints": [{"Timestamp": ' \
           '1516337100, "Average": 0.7533527893265134, "Unit": "Count/Second"}, {"Timestamp": 1516334400, "Average": ' \
           '0.7866780026666479, "Unit": "Count/Second"}, {"Timestamp": 1516335000, "Average": 0.7599913390383313, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516335900, "Average": 0.7433448670975793, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516336500, "Average": 0.7666502259311192, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516333800, "Average": 0.7533158370007051, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516334700, "Average": 0.7466729456139353, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516336800, "Average": 0.7599947235175769, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516335300, "Average": 0.7733425037695676, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516335600, "Average": 0.7533442794233036, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516334100, "Average": 0.7266630015482233, ' \
           '"Unit": "Count/Second"}, {"Timestamp": 1516336200, "Average": 0.7566506726273893, ' \
           '"Unit": "Count/Second"}], "ResponseMetadata": {"RequestId": "3f4d0937-fc91-11e7-9a68-091e021bc9b8", ' \
           '"HTTPStatusCode": 200, "HTTPHeaders": {"x-amzn-requestid": "3f4d0937-fc91-11e7-9a68-091e021bc9b8", ' \
           '"content-type": "text/xml", "content-length": "2305", "vary": "Accept-Encoding", "date": "Thu, ' \
           '18 Jan 2018 20:50:41 GMT"}, "RetryAttempts": 0}}, {"Label": "IncomingBytes", "Datapoints": [], ' \
           '"ResponseMetadata": {"RequestId": "3f5127ef-fc91-11e7-9a68-091e021bc9b8", "HTTPStatusCode": 200, ' \
           '"HTTPHeaders": {"x-amzn-requestid": "3f5127ef-fc91-11e7-9a68-091e021bc9b8", "content-type": "text/xml", ' \
           '"content-length": "336", "date": "Thu, 18 Jan 2018 20:50:41 GMT"}, "RetryAttempts": 0}}]'

def test_readMetrics(jsonString):
    openedJson = parseMetrics.readMetrics(jsonString)
    assert openedJson[0]['Label'] == "CPUUtilization"
    assert openedJson[1]['Label'] == "ReadIOPS"
    assert openedJson[2]['Label'] == "WriteIOPS"
    assert openedJson[3]['Label'] == "IncomingBytes"

def test_createLists(jsonString):
    openedJson = parseMetrics.readMetrics(jsonString)
    cpu, cpuTime, read, readTime, write, writeTime, mem, memTime= ([] for i in range(8))
    parseMetrics.createLists(openedJson[0], cpuTime, cpu)
    parseMetrics.createLists(openedJson[1], readTime, read)
    parseMetrics.createLists(openedJson[2], writeTime, write)
    parseMetrics.createLists(openedJson[3], memTime, mem)

    # Check that time lists and number of elements for data lists are consistent
    assert cpuTime == readTime == writeTime # == memTime
    assert len(cpu) == len(read) == len(write) # == len(mem)

    # Check that instantiating ParsedMetrics produces same lists
    pm = parseMetrics.ParsedMetrics(jsonString)
    assert cpu == pm.cpuList #and cpuTime == pm.cpuTimeList
    assert read == pm.readIOList
    assert write == pm.writeIOList
    # assert mem == pm.memoryList

    # Check that time list is sorted
    assert all(cpuTime[i] <= cpuTime[i + 1] for i in range(len(cpuTime) - 1)) == True

def test__sortLists():
    time = [3, 2, 5, 1, 6, 4]
    data = [4, 5, 2, 6, 1, 3]

    parseMetrics._sortLists(data, time)

    assert time == [1, 2, 3, 4, 5, 6]
    assert data == [6 ,5, 4, 3, 2, 1]