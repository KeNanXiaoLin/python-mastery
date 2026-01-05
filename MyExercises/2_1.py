import tracemalloc
import csv

# 具名元组
from collections import namedtuple


# 查看文件基础内存占用
def basic_memory_usage(filename):
    tracemalloc.clear_traces()
    tracemalloc.start()
    f = open(filename)
    data = f.read()
    print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
    tracemalloc.stop()
    return data


# 将文件的每一行转换为字符串
def read_rides_as_lists(filename):
    tracemalloc.clear_traces()
    tracemalloc.start()
    f = open(filename)
    lines = f.readlines()
    print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
    tracemalloc.stop()
    return lines


# 使用csv模块将文件的每一行转换为元组列表
def read_rides_as_tuples(filename):
    """
    Read the bus ride data as a list of tuples
    """
    tracemalloc.clear_traces()
    tracemalloc.start()
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)
    print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
    tracemalloc.stop()
    return records


# 将文件的每一行转换为字典列表
def read_rides_as_dict(filename):
    """
    Read the bus ride data as a list of dict
    """
    tracemalloc.clear_traces()
    tracemalloc.start()
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            record = {}
            record["route"] = row[0]
            record["date"] = row[1]
            record["daytype"] = row[2]
            record["rides"] = int(row[3])
            records.append(record)
    print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
    tracemalloc.stop()
    return records


# 普通类
class RowNormal:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


RowNameTuple = namedtuple("Row", ["route", "date", "daytype", "rides"])


# 带 __slots__ 的类
class RowSlot:
    __slots__ = ["route", "date", "daytype", "rides"]

    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


# 将文件的每一行转换为普通类对象列表
def read_rides_as_normal_rows(filename):
    """
    Read the bus ride data as a list of Row objects
    """
    tracemalloc.clear_traces()
    tracemalloc.start()
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            record = RowNormal(row[0], row[1], row[2], int(row[3]))
            records.append(record)
    print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
    tracemalloc.stop()
    return records


def read_rides_as_nametuple_rows(filename):
    """
    Read the bus ride data as a list of Row objects
    """
    tracemalloc.clear_traces()
    tracemalloc.start()
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            record = RowNameTuple(row[0], row[1], row[2], int(row[3]))
            records.append(record)
    print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
    tracemalloc.stop()
    return records


def read_rides_as_slot_rows(filename):
    """
    Read the bus ride data as a list of RowSlot objects
    """
    tracemalloc.clear_traces()
    tracemalloc.start()
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            record = RowSlot(row[0], row[1], row[2], int(row[3]))
            records.append(record)
    print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
    tracemalloc.stop()
    return records


if __name__ == "__main__":
    basic_memory_usage("Data/ctabus.csv")
    lines = read_rides_as_lists("Data/ctabus.csv")
    tuples = read_rides_as_tuples("Data/ctabus.csv")
    dicts = read_rides_as_dict("Data/ctabus.csv")
    rows_normal = read_rides_as_normal_rows("Data/ctabus.csv")
    rows_nametuple = read_rides_as_nametuple_rows("Data/ctabus.csv")
    rows_slot = read_rides_as_slot_rows("Data/ctabus.csv")

    print(tuples[0])
    print(lines[0])
    print(dicts[0])
    print(rows_normal[0].route)
    print(rows_nametuple[0].route)
    print(rows_slot[0].route)
