from abc import ABC, abstractmethod
import json
import csv
from typing import List, Dict


# -------------------------- 1. 定义抽象基类（核心接口） --------------------------
class DataParser(ABC):
    """
    数据解析器抽象基类：定义所有解析器必须实现的核心接口
    包含抽象方法（强制实现）+ 具体方法（子类复用）
    """

    def __init__(self, file_path: str):
        self.file_path = file_path  # 通用属性：解析文件路径
        self.data: List[Dict] = []  # 解析后的数据存储

    # 抽象方法：子类必须实现的核心解析逻辑
    @abstractmethod
    def parse(self) -> List[Dict]:
        """解析指定文件，返回结构化字典列表"""
        pass

    # 抽象方法：子类必须实现的校验逻辑
    @abstractmethod
    def validate_data(self) -> bool:
        """校验解析后的数据是否符合规范"""
        pass

    # 具体方法：所有子类可复用的通用逻辑
    def save_to_json(self, output_path: str):
        """将解析后的数据保存为JSON文件（通用功能，子类无需重写）"""
        if not self.data:
            raise ValueError("未解析数据，请先调用parse()方法")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存至 {output_path}")

    # 具体方法：通用数据过滤
    def filter_data(self, key: str, value) -> List[Dict]:
        """过滤包含指定键值对的数据（通用功能）"""
        return [item for item in self.data if item.get(key) == value]


# -------------------------- 2. 实现子类：JSON解析器 --------------------------
class JsonParser(DataParser):
    """JSON文件解析器：实现抽象基类的所有抽象方法"""

    def parse(self) -> List[Dict]:
        """解析JSON文件"""
        with open(self.file_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        print(f"JSON文件 {self.file_path} 解析完成，共{len(self.data)}条数据")
        return self.data

    def validate_data(self) -> bool:
        """校验JSON数据：确保每条数据包含'id'字段"""
        for item in self.data:
            if "id" not in item:
                raise ValueError(f"数据缺少'id'字段：{item}")
        print("JSON数据校验通过")
        return True


# -------------------------- 3. 实现子类：CSV解析器 --------------------------
class CsvParser(DataParser):
    """CSV文件解析器：实现抽象基类的所有抽象方法"""

    def parse(self) -> List[Dict]:
        """解析CSV文件"""
        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.data = list(reader)
        print(f"CSV文件 {self.file_path} 解析完成，共{len(self.data)}条数据")
        return self.data

    def validate_data(self) -> bool:
        """校验CSV数据：确保每条数据包含'name'字段"""
        for item in self.data:
            if "name" not in item:
                raise ValueError(f"数据缺少'name'字段：{item}")
        print("CSV数据校验通过")
        return True


# -------------------------- 4. 注册虚拟子类（无需继承，仅适配接口） --------------------------
# 场景：第三方YAML解析器，无法修改源码继承DataParser，通过注册虚拟子类适配接口
class ThirdPartyYamlParser:
    """第三方YAML解析器（无继承DataParser）"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = []

    def parse(self):
        """模拟YAML解析逻辑"""
        print(f"第三方YAML解析器解析 {self.file_path}")
        self.data = [{"id": 1, "name": "yaml数据"}]
        return self.data

    def validate_data(self):
        """模拟YAML数据校验"""
        print("YAML数据校验通过")
        return True


# 注册为DataParser的虚拟子类（支持isinstance/issubclass校验）
DataParser.register(ThirdPartyYamlParser)

# -------------------------- 5. 测试代码 --------------------------
if __name__ == "__main__":
    import sys

    # sys.path.append("./")
    with open("./test_data.txt", "r", encoding="utf-8") as f:
        data = f.readlines()
        print(data)
    # ========== 测试1：JSON解析器 ==========
    print("=== 测试JSON解析器 ===")
    json_parser = JsonParser(
        "test_data.json"
    )  # 需提前创建test_data.json，内容如：{"id":1,"name":"测试1"},{"id":2,"name":"测试2"}]
    json_parser.parse()
    json_parser.validate_data()
    json_parser.save_to_json("output_json.json")
    filtered = json_parser.filter_data("id", 1)
    print("过滤id=1的数据：", filtered)

    # ========== 测试2：CSV解析器 ==========
    print("\n=== 测试CSV解析器 ===")
    csv_parser = CsvParser(
        "test_data.csv"
    )  # 需提前创建test_data.csv，表头包含name，内容如：id,name\n3,测试3\n4,测试4
    csv_parser.parse()
    csv_parser.validate_data()
    csv_parser.save_to_json("output_csv.json")

    # ========== 测试3：抽象基类约束 ==========
    print("\n=== 测试抽象基类约束 ===")
    # 抽象基类无法实例化（会抛出TypeError）
    # parser = DataParser("test.txt")  # 取消注释会报错

    # ========== 测试4：虚拟子类校验 ==========
    print("\n=== 测试虚拟子类 ===")
    yaml_parser = ThirdPartyYamlParser("test.yaml")
    print("是否为DataParser实例：", isinstance(yaml_parser, DataParser))  # True
    yaml_parser.parse()
    yaml_parser.validate_data()
