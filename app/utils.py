import csv
import time
from bluetooth import discover_devices


def load_departments():
    with open('departments.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        return [dict(row) for row in csv_reader]


def get_dept_name_value():
    depts = load_departments()
    pairs = list()
    for dept in depts:
        pairs.append((dept['dept_code'], dept['dept_name']))
    return pairs


def discover_bd(seconds=10):
    t_end = time.time() + seconds
    devices = set()

    while time.time() < t_end:
        temp = discover_devices()
        devices.update(temp)
    return devices
