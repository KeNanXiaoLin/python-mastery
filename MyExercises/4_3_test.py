"""
Python描述符协议完整示例
展示描述符的内部机制、实际应用和高级用法
"""

print("=" * 80)
print("Python描述符协议完整示例")
print("=" * 80)


# ============================================================================
# 第一部分：基础描述符演示
# ============================================================================
print("\n" + "=" * 80)
print("1. 基础描述符演示")
print("=" * 80)


class LoggedAttribute:
    """基础描述符：记录所有属性访问"""

    def __init__(self, name):
        print(f"  LoggedAttribute.__init__: name={name}")
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            # 通过类访问时，返回描述符本身
            print(f"  {self.name}.__get__: 通过类访问，返回描述符")
            return self
        else:
            # 通过实例访问时，返回实际值
            print(f"  {self.name}.__get__: instance={id(instance)}, owner={owner}")
            value = instance.__dict__.get(self.name, "未设置")
            return value

    def __set__(self, instance, value):
        print(f"  {self.name}.__set__: instance={id(instance)}, value={value}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        print(f"  {self.name}.__delete__: instance={id(instance)}")
        del instance.__dict__[self.name]


class Person:
    """使用描述符的类"""

    name = LoggedAttribute("name")
    age = LoggedAttribute("age")

    def __init__(self, name, age):
        print(f"Person.__init__: name={name}, age={age}")
        self.name = name  # 触发 __set__
        self.age = age  # 触发 __set__

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        print(f"Person.__setattr__: name={name}, value={value}")

    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"


print(Person.__dict__)
print("\n创建Person实例:")
print("-" * 40)
alice = Person("Alice", 25)
print(f"alice = {alice}")
print(alice.__dict__)
print("\n访问描述符属性:")
print("-" * 40)
print(f"alice.name = {alice.name}")  # 触发 __get__
print(f"alice.age = {alice.age}")  # 触发 __get__

print("\n修改描述符属性:")
print("-" * 40)
alice.age = 26  # 触发 __set__
print(f"修改后: {alice}")

print("\n删除描述符属性:")
print("-" * 40)
del alice.age  # 触发 __delete__

print("\n通过类访问描述符:")
print("-" * 40)
print(f"Person.name = {Person.name}")  # 触发 __get__(instance=None)
print(f"Person.age = {Person.age}")  # 触发 __get__(instance=None)

print("\n查看实例字典:")
print("-" * 40)
print(f"alice.__dict__ = {alice.__dict__}")

# ============================================================================
# 第二部分：描述符与实例字典的优先级
# ============================================================================
print("\n\n" + "=" * 80)
print("2. 描述符与实例字典的优先级")
print("=" * 80)


class PriorityDemo:
    """演示描述符优先级"""

    class Descriptor:
        def __get__(self, instance, owner):
            if instance is None:
                return self
            return "来自描述符的值"

        def __set__(self, instance, value):
            print(f"描述符__set__被调用，但忽略值: {value}")

    desc = Descriptor()  # 类属性是描述符


print("\n创建实例:")
print("-" * 40)
obj = PriorityDemo()

print("\n1. 描述符优先级高于实例字典:")
print("-" * 40)
print(f"obj.desc = {obj.desc}")  # 触发描述符的__get__

# 尝试直接修改实例字典
obj.__dict__["desc"] = "直接存储在实例字典中的值"
print(f"设置 obj.__dict__['desc'] = '直接存储在实例字典中的值'")
print(f"obj.desc = {obj.desc}")  # 仍然触发描述符，描述符优先级更高!

print("\n2. 删除实例字典中的值:")
print("-" * 40)
del obj.__dict__["desc"]
print(f"删除后 obj.desc = {obj.desc}")

print("\n3. 方法描述符（只有__get__）的优先级:")
print("-" * 40)


class MethodOnlyDescriptor:
    """只有__get__的描述符（方法描述符）"""

    def __get__(self, instance, owner):
        return "来自方法描述符"


class TestClass:
    method_desc = MethodOnlyDescriptor()


test = TestClass()
print(f"test.method_desc = {test.method_desc}")

# 在实例字典中添加同名属性
test.__dict__["method_desc"] = "实例字典中的值"
print(f"设置 test.__dict__['method_desc'] = '实例字典中的值'")
print(f"test.method_desc = {test.method_desc}")  # 实例字典优先！


# ============================================================================
# 第三部分：数据存储描述符（常见模式）
# ============================================================================
print("\n\n" + "=" * 80)
print("3. 数据存储描述符")
print("=" * 80)


class Field:
    """将数据存储在实例字典中的描述符"""

    def __init__(self, name=None):
        print(f"  Field.__init__: name={name}")
        self.name = name

    def __set_name__(self, owner, name):
        """Python 3.6+: 自动设置属性名"""
        print(f"  Field.__set_name__: owner={owner.__name__}, name={name}")
        if self.name is None:
            self.name = name
        # 在所有者类中存储字段信息
        if not hasattr(owner, "_fields"):
            owner._fields = []
        owner._fields.append(self.name)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # 如果属性不存在，返回默认值而不是抛出AttributeError
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        # 简单的类型检查
        if self.name.endswith("_count") and not isinstance(value, int):
            raise TypeError(f"{self.name} 必须是整数")
        instance.__dict__[self.name] = value


class Product:
    """使用Field描述符的类"""

    # 使用自动命名
    name = Field()
    price = Field()
    stock_count = Field()  # 需要整数

    def __init__(self, name, price, stock_count):
        self.name = name
        self.price = price
        self.stock_count = stock_count

    def __repr__(self):
        return f"Product({self.name}, ${self.price}, 库存: {self.stock_count})"


print("\n创建Product实例:")
print("-" * 40)
laptop = Product("Laptop", 999.99, 10)
print(f"laptop = {laptop}")

print(f"\nProduct._fields = {Product._fields}")
print(f"laptop.__dict__ = {laptop.__dict__}")

print("\n测试类型检查:")
print("-" * 40)
try:
    laptop.stock_count = "不是整数"  # 会触发TypeError
except TypeError as e:
    print(f"错误: {e}")

print("\n访问不存在的属性:")
print("-" * 40)
print(f"laptop.nonexistent = {getattr(laptop, 'nonexistent', '默认值')}")

# ============================================================================
# 第四部分：延迟计算属性（缓存模式）
# ============================================================================
print("\n\n" + "=" * 80)
print("4. 延迟计算属性（缓存模式）")
print("=" * 80)


class CachedProperty:
    """缓存昂贵的计算结果"""

    def __init__(self, func):
        print(f"  CachedProperty.__init__: func={func.__name__}")
        self.func = func
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # 检查是否已缓存
        cache_attr = f"_{self.name}_cached"
        if hasattr(instance, cache_attr):
            print(f"  {self.name}: 返回缓存值")
            return getattr(instance, cache_attr)

        # 计算并缓存
        print(f"  {self.name}: 计算新值")
        value = self.func(instance)
        setattr(instance, cache_attr, value)
        return value

    # 没有__set__方法，所以是只读属性


class ExpensiveData:
    """有昂贵计算的数据类"""

    def __init__(self, data):
        self.data = data

    @CachedProperty
    def processed_data(self):
        """模拟昂贵的计算过程"""
        print("  执行昂贵的计算...")
        # 模拟耗时计算
        import time

        time.sleep(0.5)  # 模拟0.5秒计算
        return [x * 2 for x in self.data if x % 2 == 0]

    @CachedProperty
    def summary(self):
        """另一个昂贵计算"""
        print("  计算摘要...")
        return f"数据长度: {len(self.data)}, 总和: {sum(self.data)}"


print("\n创建ExpensiveData实例:")
print("-" * 40)
data_obj = ExpensiveData([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

print("\n第一次访问缓存属性:")
print("-" * 40)
result1 = data_obj.processed_data
print(f"processed_data = {result1}")

print("\n第二次访问（应该从缓存获取）:")
print("-" * 40)
result2 = data_obj.processed_data
print(f"processed_data = {result2}")
print(f"result1 is result2? {result1 is result2}")

print("\n访问另一个缓存属性:")
print("-" * 40)
print(f"summary = {data_obj.summary}")

print("\n查看实例的缓存:")
print("-" * 40)
print(f"data_obj.__dict__.keys() = {list(data_obj.__dict__.keys())}")


# ============================================================================
# 第五部分：验证描述符
# ============================================================================
print("\n\n" + "=" * 80)
print("5. 验证描述符")
print("=" * 80)


class Typed:
    """类型验证描述符"""

    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"'{self.name}' 必须是 {self.expected_type.__name__}，而不是 {type(value).__name__}"
            )
        instance.__dict__[self.name] = value


class Range:
    """范围验证描述符"""

    def __init__(self, name, min_value=None, max_value=None):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"'{self.name}' 不能小于 {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"'{self.name}' 不能大于 {self.max_value}")
        instance.__dict__[self.name] = value


class Student:
    """使用验证描述符的类"""

    name = Typed("name", str)
    age = Typed("age", int)
    grade = Range("grade", min_value=0, max_value=100)

    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def __repr__(self):
        return f"Student({self.name}, {self.age}岁, 成绩: {self.ggrade})"


print("\n创建Student实例:")
print("-" * 40)
try:
    student = Student("张三", 18, 85)
    print(f"student = {student}")
except Exception as e:
    print(f"错误: {e}")

print("\n测试类型验证:")
print("-" * 40)
try:
    student.age = "不是整数"  # 应该失败
except TypeError as e:
    print(f"类型错误: {e}")

print("\n测试范围验证:")
print("-" * 40)
try:
    student.grade = 150  # 应该失败
except ValueError as e:
    print(f"范围错误: {e}")


# ============================================================================
# 第六部分：方法描述符（函数如何工作）
# ============================================================================
print("\n\n" + "=" * 80)
print("6. 方法描述符（函数如何工作）")
print("=" * 80)

print("\n演示函数作为描述符:")
print("-" * 40)


class MyClass:
    def method(self):
        return f"method called with self={self}"


obj = MyClass()

print(f"1. 函数对象本身: {MyClass.method}")
print(f"2. 函数有__get__方法? {hasattr(MyClass.method, '__get__')}")

print("\n手动模拟方法绑定:")
print("-" * 40)
# 从类字典获取原始函数
raw_function = MyClass.__dict__["method"]
print(f"原始函数: {raw_function}")

# 使用描述符协议创建绑定方法
bound_method = raw_function.__get__(obj, MyClass)
print(f"绑定方法: {bound_method}")

# 调用绑定方法
result = bound_method()
print(f"调用结果: {result}")

print("\n对比直接调用:")
print("-" * 40)
print(f"obj.method() = {obj.method()}")
print(f"obj.method 是 bound_method? {obj.method is bound_method}")

# ============================================================================
# 第七部分：描述符冲突与协调
# ============================================================================
print("\n\n" + "=" * 80)
print("7. 描述符冲突与协调")
print("=" * 80)

print("\n描述符不能共享同一个属性名:")
print("-" * 40)


class DescriptorA:
    def __get__(self, instance, owner):
        return "来自DescriptorA"


class DescriptorB:
    def __get__(self, instance, owner):
        return "来自DescriptorB"


try:

    class ConflictClass:
        x = DescriptorA()
        x = DescriptorB()  # DescriptorB覆盖DescriptorA

    obj = ConflictClass()
    print(f"ConflictClass.x = {obj.x}")  # 只显示最后一个
    print("注意: 后定义的描述符覆盖先定义的")
except Exception as e:
    print(f"错误: {e}")

print("\n描述符与__slots__冲突:")
print("-" * 40)

try:

    class SlotConflict:
        __slots__ = ["x", "y"]
        z = DescriptorA()  # 错误: 与__slots__冲突

    obj = SlotConflict()
    print(f"obj.z = {obj.z}")
except ValueError as e:
    print(f"ValueError: {e}")


exit()
# ============================================================================
# 第八部分：描述符实际应用 - 微型ORM
# ============================================================================
print("\n\n" + "=" * 80)
print("8. 描述符实际应用 - 微型ORM")
print("=" * 80)


class Column:
    """数据库列描述符"""

    def __init__(self, column_type, primary_key=False, nullable=True):
        self.column_type = column_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name
        # 在元类中注册列信息
        if not hasattr(owner, "_columns"):
            owner._columns = {}
        owner._columns[name] = self

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        # 简单的类型检查
        if value is None and not self.nullable:
            raise ValueError(f"{self.name} 不能为None")
        instance.__dict__[self.name] = value

    def to_sql(self):
        """生成SQL列定义"""
        sql = f"{self.name} {self.column_type}"
        if not self.nullable:
            sql += " NOT NULL"
        if self.primary_key:
            sql += " PRIMARY KEY"
        return sql


class ModelMeta(type):
    """模型元类，收集所有Column描述符"""

    def __new__(cls, name, bases, attrs):
        # 创建新类
        new_class = super().__new__(cls, name, bases, attrs)

        # 确保有_columns字典
        if not hasattr(new_class, "_columns"):
            new_class._columns = {}

        # 从父类继承列
        for base in bases:
            if hasattr(base, "_columns"):
                new_class._columns.update(base._columns)

        # 收集当前类的列
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Column):
                if attr_value.name is None:
                    attr_value.name = attr_name

        return new_class


class Model(metaclass=ModelMeta):
    """所有模型的基类"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create_table_sql(cls):
        """生成创建表的SQL"""
        columns = [col.to_sql() for col in cls._columns.values()]
        return (
            f"CREATE TABLE {cls.__name__.lower()} (\n  "
            + ",\n  ".join(columns)
            + "\n);"
        )

    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class User(Model):
    """用户模型"""

    id = Column("INTEGER", primary_key=True)
    username = Column("VARCHAR(50)", nullable=False)
    email = Column("VARCHAR(100)")
    age = Column("INTEGER")


print("\n创建User实例:")
print("-" * 40)
user = User(id=1, username="alice", email="alice@example.com", age=25)
print(f"user = {user}")

print("\n生成创建表SQL:")
print("-" * 40)
print(User.create_table_sql())

print("\n查看模型结构:")
print("-" * 40)
print(f"User._columns = {User._columns}")

print("\n测试验证:")
print("-" * 40)
try:
    user.username = None  # 应该失败，因为nullable=False
except ValueError as e:
    print(f"验证错误: {e}")

print("\n" + "=" * 80)
print("描述符总结")
print("=" * 80)
print(
    """
关键要点:
1. 描述符控制点运算符(.)的行为
2. 优先级: 数据描述符 > 实例字典 > 非数据描述符
3. __get__接收instance和owner参数
4. 描述符本身不存储数据，数据在实例中
5. 函数、property、classmethod都是描述符
6. __set_name__自动设置属性名(Python 3.6+)
7. 描述符是Python高级特性的基础
"""
)
print("=" * 80)
