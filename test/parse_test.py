import parseMetrics
import importlib

file_name_1 = "metric_files/metric-file.txt"
file_name_2 = "metric_files/metric-file-2.txt"

ex_cpu_list_1 = [2.19147911456887, 2.468315272760944, 2.433574140965086, 2.259887005649732, 2.566379549874962, 2.35871075298693, 2.333592664629064, 2.2008057793831517, 2.440677966101698, 2.36607390941929, 2.2341576363804743, 2.2745762711864463]
ex_cpu_time_list_1 = [1516335600, 1516334100, 1516336200, 1516337100, 1516334400, 1516335000, 1516335900, 1516336500, 1516333800, 1516334700, 1516336800, 1516335300]
ex_readIO_list_1 = [0.23336444859314573, 0.33999999999999997, 0.23334111137037902, 0.23333333333333334, 0.23330611428666653, 0.2366546117397804, 0.2333294445092582, 0.23334500058336252, 0.23335666900023339, 0.23333333333333334, 0.2333294445092582, 0.2366355597031507]
ex_readIO_time_list_1 = [1516337100, 1516334400, 1516335000, 1516335900, 1516336500, 1516333800, 1516334700, 1516336800, 1516335300, 1516335600, 1516334100, 1516336200]
ex_writeIO_list_1 = [0.7533527893265134, 0.7866780026666479, 0.7599913390383313, 0.7433448670975793, 0.7666502259311192, 0.7533158370007051, 0.7466729456139353, 0.7599947235175769, 0.7733425037695676, 0.7533442794233036, 0.7266630015482233, 0.7566506726273893]
ex_writeIO_time_list_1 = [1516337100, 1516334400, 1516335000, 1516335900, 1516336500, 1516333800, 1516334700, 1516336800, 1516335300, 1516335600, 1516334100, 1516336200]
ex_memory_list_1 = []
ex_memory_time_list_1 = []

ex_cpu_list_2 = [2.19147911456887]
ex_cpu_time_list_2 = [1516335600]
ex_readIO_list_2 = [0.23336444859314573]
ex_readIO_time_list_2 = [1516337100]
ex_writeIO_list_2 = [0.7533527893265134]
ex_writeIO_time_list_2 = [1516337100]
ex_memory_list_2 = []
ex_memory_time_list_2 = []


# def test_parse_1():
#     file_data = parseMetrics.readMetricsFile(file_name_1)
#     parseMetrics.createCPULists(file_data)
#     parseMetrics.createReadIOLists(file_data)
#     parseMetrics.createWriteIOLists(file_data)
#     parseMetrics.createMemLists(file_data)
#     assert parseMetrics.cpuList == ex_cpu_list_1
#     assert parseMetrics.cpuTimeList == ex_cpu_time_list_1
#     assert parseMetrics.readIOList == ex_readIO_list_1
#     assert parseMetrics.readIOTimeList == ex_readIO_time_list_1
#     assert parseMetrics.writeIOList == ex_writeIO_list_1
#     assert parseMetrics.writeIOTimeList == ex_writeIO_time_list_1
#     assert parseMetrics.memoryList == ex_memory_list_1
#     assert parseMetrics.memoryTimeList == ex_memory_time_list_1
#     importlib.reload(parseMetrics)
#
# def test_parse_2():
#     file_data = parseMetrics.readMetricsFile(file_name_2)
#     parseMetrics.createCPULists(file_data)
#     parseMetrics.createReadIOLists(file_data)
#     parseMetrics.createWriteIOLists(file_data)
#     parseMetrics.createMemLists(file_data)
#     assert parseMetrics.cpuList == ex_cpu_list_2
#     assert parseMetrics.cpuTimeList == ex_cpu_time_list_2
#     assert parseMetrics.readIOList == ex_readIO_list_2
#     assert parseMetrics.readIOTimeList == ex_readIO_time_list_2
#     assert parseMetrics.writeIOList == ex_writeIO_list_2
#     assert parseMetrics.writeIOTimeList == ex_writeIO_time_list_2
#     assert parseMetrics.memoryList == ex_memory_list_2
#     assert parseMetrics.memoryTimeList == ex_memory_time_list_2
#     importlib.reload(parseMetrics)

def test_parse_3():
   metrics = parseMetrics.ParsedMetrics(file_name_1)
   assert len(metrics.cpuList) > 0