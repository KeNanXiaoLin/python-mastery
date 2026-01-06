# readport.py

import csv
import tracemalloc


# 读取文件并转换为字典列表的函数
def read_portfolio(filename):
    portfolio = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            record = {
                "name": row[0],  # 股票名称
                "shares": int(row[1]),  # 持股数量
                "price": float(row[2]),  # 购买价格
            }
            portfolio.append(record)
    return portfolio


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


if __name__ == "__main__":
    portfolio = read_portfolio("Data/portfolio.csv")
    from pprint import pprint

    pprint(portfolio)
    rides = read_rides_as_dict("Data/ctabus.csv")
    # problem 1 芝加哥一共有多少条公交路线 使用set去重
    print("Problem 1:")
    routes = set()
    for ride in rides:
        routes.add(ride["route"])
    print(len(routes))
    # problem 2 2011 年 2 月 2 日，22 路公交车的载客量是多少？任选一条线路、一个日期，查询其载客量。
    print("Problem 2:")
    for ride in rides:
        if ride["route"] == "22" and ride["date"] == "02/02/2011":
            print(ride["rides"])
            break
    # problem 3 统计每条线路的总载客量，找出载客量最大的线路
    print("Problem 3:")
    from collections import defaultdict

    dic = defaultdict(int)
    for ride in rides:
        dic[ride["route"]] += ride["rides"]
    # 对值进行从大到小的排序
    sorted_dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    print(sorted_dic[:10])
    # problem 4 2001 年至 2011 年这十年间，载客量增长最多的五条公交线路是哪些？
    print("Problem 4:")
    # 先统计2001年的
    dic = defaultdict(int)
    for ride in rides:
        if ride["date"].endswith("2001"):
            dic[ride["route"]] += ride["rides"]

    # 再统计2011年的
    dic2 = defaultdict(int)
    for ride in rides:
        if ride["date"].endswith("2011"):
            dic2[ride["route"]] += ride["rides"]

    # 计算2001年至2011年的增长量
    growth = {}
    for route in dic2:
        if route in dic:
            growth[route] = dic2[route] - dic[route]
        else:
            growth[route] = dic2[route]
    # 对增长量进行从大到小的排序
    sorted_growth = sorted(growth.items(), key=lambda x: x[1], reverse=True)
    print(sorted_growth[:10])
