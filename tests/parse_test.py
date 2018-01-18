import parse_class.py

file_name_1 = "file1.txt"
correct_file_1 = "answer2.txt"

file_name_2 = "file2.txt"
correct_file_2 = "answer2.txt"

def parse(logfile):
    return parse_class.parse_method(logfile)

def test_parse():
    assert parse(file_name_1) == correct_file_1
    assert parse(file_name_2) == correct_file_2