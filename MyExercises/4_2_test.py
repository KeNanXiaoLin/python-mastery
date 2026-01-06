"""
Python继承机制完整示例
展示MRO、super()和多重继承的协同工作
"""

print("=" * 70)
print("Python继承机制完整示例")
print("=" * 70)


# ============================================================================
# 第一部分：单继承和MRO
# ============================================================================
print("\n" + "=" * 70)
print("1. 单继承和MRO（方法解析顺序）")
print("=" * 70)


class Animal:
    def __init__(self, name):
        print(f"  Animal.__init__ called for {name}")
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

    def move(self):
        return f"{self.name} moves"


class Mammal(Animal):
    def __init__(self, name, fur_color):
        print(f"  Mammal.__init__ called for {name}")
        super().__init__(name)  # 调用父类初始化
        self.fur_color = fur_color

    def speak(self):
        # 扩展父类方法
        parent_result = super().speak()
        return f"{parent_result}, specifically a mammal sound"

    def feed_milk(self):
        return f"{self.name} feeds milk"


class Dog(Mammal):
    def __init__(self, name, fur_color, breed):
        print(f"  Dog.__init__ called for {name}")
        super().__init__(name, fur_color)  # 调用父类初始化
        self.breed = breed

    def speak(self):
        # 再次扩展
        parent_result = super().speak()
        return f"{parent_result}, and barks!"

    def fetch(self):
        return f"{self.name} fetches the ball"


print("\n创建Dog实例:")
buddy = Dog("Buddy", "brown", "Golden Retriever")

print(f"\nbuddy.speak(): {buddy.speak()}")
print(f"buddy.move(): {buddy.move()}")
print(f"buddy.feed_milk(): {buddy.feed_milk()}")

# 查看MRO
print("\n继承链的MRO:")
print(f"Dog.__mro__: {Dog.__mro__}")
print(f"Mammal.__mro__: {Mammal.__mro__}")
print(f"Animal.__mro__: {Animal.__mro__}")

# 手动模拟属性查找
print("\n属性查找过程模拟:")


def find_attribute(cls, attr_name):
    """模拟Python的属性查找过程"""
    for c in cls.__mro__:
        if attr_name in c.__dict__:
            return c
    return None


print(f"'speak'方法在Dog MRO中位于: {find_attribute(Dog, 'speak')}")
print(f"'move'方法在Dog MRO中位于: {find_attribute(Dog, 'move')}")
print(f"'feed_milk'方法在Dog MRO中位于: {find_attribute(Dog, 'feed_milk')}")


# ============================================================================
# 第二部分：多重继承和菱形继承
# ============================================================================
print("\n\n" + "=" * 70)
print("2. 多重继承和菱形继承")
print("=" * 70)


class Engine:
    def __init__(self, horsepower):
        print(f"  Engine.__init__: {horsepower}HP")
        self.horsepower = horsepower

    def start(self):
        return "Engine starts: Vroom!"

    def stop(self):
        return "Engine stops"


class ElectricMotor:
    def __init__(self, voltage):
        print(f"  ElectricMotor.__init__: {voltage}V")
        self.voltage = voltage

    def start(self):
        return "Electric motor starts: Whirr!"

    def charge(self):
        return "Charging battery"


class Vehicle:
    def __init__(self, make, model):
        print(f"  Vehicle.__init__: {make} {model}")
        self.make = make
        self.model = model
        self.speed = 0

    def drive(self):
        return f"{self.make} {self.model} is driving"


# 普通多重继承
class Car(Vehicle, Engine):
    def __init__(self, make, model, horsepower):
        print(f"  Car.__init__")
        # 必须手动协调多个父类的初始化
        Vehicle.__init__(self, make, model)
        Engine.__init__(self, horsepower)

    def start(self):
        return f"Car: {Engine.start(self)}"


# 菱形继承 - 使用super()实现协同
print("\n菱形继承示例:")


class PoweredDevice:
    def __init__(self, power_source):
        print(f"  PoweredDevice.__init__: {power_source}")
        self.power_source = power_source

    def turn_on(self):
        return "Powered device turns on"


class Scanner(PoweredDevice):
    def __init__(self, power_source, dpi):
        print(f"  Scanner.__init__")
        super().__init__(power_source)  # 使用super()
        self.dpi = dpi

    def turn_on(self):
        result = super().turn_on()
        return f"{result}, scanner ready"


class Printer(PoweredDevice):
    def __init__(self, power_source, pages_per_minute):
        print(f"  Printer.__init__")
        super().__init__(power_source)  # 使用super()
        self.pages_per_minute = pages_per_minute

    def turn_on(self):
        result = super().turn_on()
        return f"{result}, printer ready"


class MultiFunctionDevice(Scanner, Printer):
    def __init__(self, power_source, dpi, pages_per_minute):
        print(f"  MultiFunctionDevice.__init__")
        # 只调用一次super()，但会协调所有父类
        super().__init__(power_source, dpi, pages_per_minute)

    def turn_on(self):
        result = super().turn_on()
        return f"{result}, MFD ready for all tasks"


print("\n创建MultiFunctionDevice实例:")
mfd = MultiFunctionDevice("AC", 1200, 30)

print(f"\nmfd.turn_on(): {mfd.turn_on()}")
print(f"mfd实例属性: {mfd.__dict__}")

# 查看MRO
print(f"\nMultiFunctionDevice.__mro__:")
for i, cls in enumerate(MultiFunctionDevice.__mro__):
    print(f"  {i}. {cls.__name__}")


# ============================================================================
# 第三部分：super()的深入理解
# ============================================================================
print("\n\n" + "=" * 70)
print("3. super()的深入理解")
print("=" * 70)


class A:
    def method(self):
        print("  A.method")
        return "A"


class B(A):
    def method(self):
        print("  B.method")
        result = super().method()  # 调用A.method
        return f"B → {result}"


class C(A):
    def method(self):
        print("  C.method")
        result = super().method()  # 调用A.method
        return f"C → {result}"


class D(B, C):
    def method(self):
        print("  D.method")
        result = super().method()  # 按MRO调用下一个类
        return f"D → {result}"


print("\n创建D实例:")
d = D()

print(f"\nD.__mro__: {D.__mro__}")
print(f"\n调用d.method():")
result = d.method()
print(f"结果: {result}")

# 验证super()不是直接调用父类
print("\n验证super()不是直接调用父类:")
print(f"D.__mro__中B之后是: {D.__mro__[D.__mro__.index(B)+1]}")
print(
    f"所以B中的super().method()调用的是: {D.__mro__[D.__mro__.index(B)+1].__name__}.method()"
)


# ============================================================================
# 第四部分：继承设计的黄金法则
# ============================================================================
print("\n\n" + "=" * 70)
print("4. 继承设计的黄金法则演示")
print("=" * 70)

print("\n法则1: 方法参数必须兼容")


class BaseLogger:
    def log(self, message, level="INFO"):
        """基类方法 - 所有子类必须保持兼容签名"""
        print(f"[{level}] {message}")


class FileLogger(BaseLogger):
    def log(self, message, level="INFO", filename=None):
        """✅ 正确: 添加额外参数，但提供默认值保持兼容"""
        super().log(message, level)
        if filename:
            print(f"  (写入文件: {filename})")


class BadLogger(BaseLogger):
    def log(self, message):
        """❌ 错误: 缺少level参数，破坏兼容性"""
        # 如果使用super()，会传递错误的参数数量
        pass


print("\n创建FileLogger实例:")
file_logger = FileLogger()
file_logger.log("系统启动", "DEBUG", "app.log")

print("\n\n法则2: 方法链必须有终止点")


class AbstractWorker:
    def process(self, data):
        """抽象基类 - 提供终止点"""
        raise NotImplementedError("子类必须实现process方法")


class DataCleaner(AbstractWorker):
    def process(self, data):
        """具体实现 - 不需要调用super()"""
        print(f"DataCleaner: 清理数据")
        return data.strip()


class DataValidator(DataCleaner):
    def process(self, data):
        """可以但不需要调用super()"""
        print(f"DataValidator: 验证数据")
        # 可以选择不调用super()，因为DataCleaner.process是完整实现
        return super().process(data) if data else None


print("\n创建DataValidator实例:")
validator = DataValidator()
result = validator.process("  test data  ")
print(f"处理结果: '{result}'")

print("\n\n法则3: 必须一致使用super()")


class Component:
    def __init__(self, id):
        print(f"  Component.__init__: {id}")
        self.id = id


class NetworkComponent(Component):
    def __init__(self, id, ip_address):
        print(f"  NetworkComponent.__init__: {id}")
        # ✅ 正确: 使用super()
        super().__init__(id)
        self.ip_address = ip_address


class SecureComponent(Component):
    def __init__(self, id, encryption_key):
        print(f"  SecureComponent.__init__: {id}")
        # ✅ 正确: 使用super()
        super().__init__(id)
        self.encryption_key = encryption_key


class SecureNetworkComponent(NetworkComponent, SecureComponent):
    def __init__(self, id, ip_address, encryption_key):
        print(f"  SecureNetworkComponent.__init__: {id}")
        # 只需调用一次super()，会自动协调所有父类
        super().__init__(id, ip_address, encryption_key)


print("\n创建SecureNetworkComponent实例:")
secure_comp = SecureNetworkComponent("server1", "192.168.1.1", "secret123")
print(f"实例属性: {secure_comp.__dict__}")


# ============================================================================
# 第五部分：实际应用 - Mixin模式
# ============================================================================
print("\n\n" + "=" * 70)
print("5. 实际应用: Mixin模式")
print("=" * 70)


# Mixin类：提供单一、可重用功能
class JSONSerializableMixin:
    """为类添加JSON序列化功能"""

    def to_json(self):
        import json

        # 收集所有可序列化的属性
        data = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                data[key] = value
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str):
        import json

        data = json.loads(json_str)
        return cls(**data)


class LoggableMixin:
    """为类添加日志功能"""

    def log(self, message):
        print(f"[LOG] {self.__class__.__name__}: {message}")


class EquatableMixin:
    """为类添加相等比较功能"""

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__


# 基础业务类
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def display(self):
        return f"{self.name}: ${self.price:.2f}"


# 使用Mixin组合功能
class EnhancedProduct(JSONSerializableMixin, LoggableMixin, EquatableMixin, Product):
    def __init__(self, name, price, sku):
        super().__init__(name, price)
        self.sku = sku

    def display(self):
        result = super().display()
        return f"{result} (SKU: {self.sku})"


print("\n创建EnhancedProduct实例:")
product1 = EnhancedProduct("Laptop", 999.99, "LP123")
product2 = EnhancedProduct("Laptop", 999.99, "LP123")

# 使用Mixin功能
print(f"product1.display(): {product1.display()}")
print(f"product1.to_json(): {product1.to_json()}")
product1.log("产品已创建")

print(f"\nproduct1 == product2? {product1 == product2}")

# 查看MRO
print(f"\nEnhancedProduct.__mro__:")
for cls in EnhancedProduct.__mro__:
    print(f"  {cls.__name__}")


# ============================================================================
# 第六部分：常见陷阱和解决方案
# ============================================================================
print("\n\n" + "=" * 70)
print("6. 常见陷阱和解决方案")
print("=" * 70)

print("\n陷阱1: 直接调用父类方法（破坏协同继承）")


class ParentA:
    def setup(self):
        print("ParentA.setup")
        self.value = "A"


class ParentB:
    def setup(self):
        print("ParentB.setup")
        self.value = "B"


class ChildWrong(ParentA, ParentB):
    def setup(self):
        print("ChildWrong.setup")
        # ❌ 错误: 直接调用指定父类
        ParentA.setup(self)
        # ParentB.setup永远不会被调用!


class ChildRight(ParentA, ParentB):
    def setup(self):
        print("ChildRight.setup")
        # ✅ 正确: 使用super()
        super().setup()


print("\n演示错误方式:")
child_wrong = ChildWrong()
child_wrong.setup()
print(f"child_wrong.value: {child_wrong.value}")

print("\n演示正确方式:")
child_right = ChildRight()
child_right.setup()
print(f"child_right.value: {child_right.value}")

print("\n陷阱2: 方法签名不兼容")


class Database:
    def query(self, sql, params=None):
        """基础查询方法"""
        print(f"Database.query: {sql}")
        return "query_result"


class CachingDatabase(Database):
    def query(self, sql, params=None, use_cache=True):
        """添加缓存参数"""
        if use_cache:
            print(f"检查缓存: {sql}")
        # ✅ 正确: 保持参数兼容
        return super().query(sql, params)


print("\n创建CachingDatabase实例:")
db = CachingDatabase()
result = db.query("SELECT * FROM users", params=[], use_cache=True)
print(f"查询结果: {result}")

print("\n" + "=" * 70)
print("总结: 继承最佳实践")
print("=" * 70)
print("1. 始终使用 super() 而不是直接调用父类")
print("2. 保持方法参数兼容（使用关键字参数和默认值）")
print("3. 确保继承链有明确的终止点")
print("4. 使用Mixin提供可重用功能")
print("5. 理解并利用MRO进行设计")
print("6. 优先使用组合而非深度继承")
print("=" * 70)
