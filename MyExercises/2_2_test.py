if __name__ == "__main__":
    names = {"IBM", "YHOO", "IBM", "CAT", "MSFT", "CAT", "IBM"}
    unique_names = set(names)
    print(unique_names)  # {'YHOO', 'MSFT', 'CAT', 'IBM'}
    members = {"YHOO", "MSFT", "CAT"}
    members.add("GOOG")  # {'YHOO', 'MSFT', 'CAT', 'GOOG'}
    members.remove("YHOO")  # {'MSFT', 'CAT', 'GOOG'}
    if "MSFT" in members:
        print("MSFT is a member")
    # 字典
    prices = {"IBM": 91.1, "MSFT": 27.72, "GOOG": 525.5}
    # 查找表
    print(prices["MSFT"])  # 27.72
    # 带默认值的查找
    print(prices.get("YHOO", 0.0))  # 0.0
    # 插入或更新
    prices["YHOO"] = 39.28
    if "YHOO" in prices:
        print(prices["YHOO"])  # 39.28
    # 使用元祖作为字典的键
    stock_prices = {
        ("IBM", "2018-12-24"): 91.1,
        ("MSFT", "2018-12-24"): 27.72,
        ("GOOG", "2018-12-24"): 525.5,
    }
    print(stock_prices[("IBM", "2018-12-24")])  # 91.1
    from collections import defaultdict

    # 缺失字典键的自动初始化
    dic = defaultdict(list)
    dic["a"] = [1, 2, 3]
    dic["b"] = [4, 5, 6]
    print(dic["a"])  # [1, 2, 3]
    print(dic["b"])  # [4, 5, 6]
    print(dic["c"])  # []
    # 支持组合操作
    dic["c"].append(7)
    print(dic["c"])  # [7]
    from collections import Counter

    totals = Counter()
    # 统计元素出现次数
    totals["IBM"] += 100
    totals["MSFT"] += 200
    print(totals)  # Counter({'MSFT': 200, 'IBM': 100})
    # 可以进行排序(默认按出现次数降序)
    print(totals.most_common(2))  # [('MSFT', 200), ('IBM', 100)]
    # 可以使用序列进行初始化，统计序列中元素出现次数
    totals = Counter(["IBM", "MSFT", "IBM", "CAT", "MSFT", "CAT", "IBM"])
    print(totals)  # Counter({'IBM': 3, 'MSFT': 2, 'CAT': 2})

    from collections import deque

    # 双端队列
    q = deque()
    q.append(1)  # 队尾添加元素 [1]
    q.append(2)  # 队尾添加元素 [1, 2]
    q.appendleft(3)  # 队头添加元素 [3, 1, 2]
    q.appendleft(4)  # 队头添加元素 [4, 3, 1, 2]
    q.pop()  # 队尾弹出元素 [4, 3, 1]
    q.popleft()  # 队头弹出元素 [3, 1]
    print(q)

    from collections import ChainMap

    # 定义多个字典
    dict1 = {"a": 1, "b": 2}
    dict2 = {"b": 3, "c": 4}
    dict3 = {"d": 5}

    # 链式合并
    combined = ChainMap(dict1, dict2, dict3)

    # 1. 读取数据：按顺序查找，dict1的'b'优先于dict2的'b'
    print(combined["a"])  # 输出 1（来自dict1）
    print(combined["b"])  # 输出 2（来自dict1，而非dict2的3）
    print(combined["c"])  # 输出 4（来自dict2）
    print(combined["d"])  # 输出 5（来自dict3）

    # 2. 修改数据：只影响第一个字典dict1
    combined["b"] = 20
    print(dict1["b"])  # 输出 20（dict1被修改）
    print(dict2["b"])  # 输出 3（dict2无变化）

    # 3. 新增数据：也只添加到第一个字典
    combined["e"] = 6
    print(dict1)  # 输出 {'a': 1, 'b': 20, 'e': 6}
    print(combined)

    # 4. 查看所有键（去重，按从右到左的顺序）
    print(list(combined.keys()))  # 输出 ['d', 'b', 'c', 'a', 'e']
    # 虽然看上去从右到左是保留了第二个字典的值，但是实际上是保留了第一个字典的值
    print(list(combined.values()))  # 输出 [5, 20, 4, 1, 6]
    a = (x * x for x in range(100))
    b = [x for x in a]
    print(type(a), a.__sizeof__())  # <class 'generator'> 184
    print(type(b), b.__sizeof__())  # <class 'list'> 904
