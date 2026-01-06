"""
Python对象与字典关系示例
展示实例字典(__dict__)、类字典和继承机制
"""

import sys

print("=" * 60)
print("Python对象与字典关系完整示例")
print("=" * 60)


# 1. 定义一个简单的类
class Person:
    """Person类 - 展示基本的对象字典关系"""

    # 类变量 - 存储在类字典中
    species = "Human"
    population = 0

    def __init__(self, name, age):
        """初始化实例"""
        self.name = name  # 这些赋值会进入实例的__dict__
        self.age = age
        Person.population += 1  # 修改类变量

    def greet(self):
        """实例方法"""
        return f"Hello, I'm {self.name}, {self.age} years old."

    @classmethod
    def get_population(cls):
        """类方法"""
        return f"Total population: {cls.population}"

    @staticmethod
    def is_adult(age):
        """静态方法"""
        return age >= 18


print("\n1. 创建Person类实例并查看字典")
print("-" * 40)

# 创建两个实例
alice = Person("Alice", 25)
bob = Person("Bob", 30)

print(f"alice实例: {alice}")
print(f"bob实例: {bob}")

print(f"\nalice.__dict__: {alice.__dict__}")
print(f"bob.__dict__: {bob.__dict__}")
print(f"Person.__dict__ 键: {list(Person.__dict__.keys())}")


# 2. 展示属性访问如何工作
print("\n\n2. 属性访问机制演示")
print("-" * 40)


def explain_attribute_lookup(obj, attr_name):
    """解释属性查找过程"""
    print(f"\n查找 {obj}.{attr_name}:")

    # 第一步：检查实例字典
    if attr_name in obj.__dict__:
        print(f"  1. 在实例__dict__中找到: {obj.__dict__[attr_name]}")
        return obj.__dict__[attr_name]

    # 第二步：检查类字典
    elif attr_name in obj.__class__.__dict__:
        print(f"  2. 在类__dict__中找到: {obj.__class__.__dict__[attr_name]}")
        return obj.__class__.__dict__[attr_name]

    # 第三步：检查基类（如果有）
    # 这里只往上查找一级基类，实际上会递归查找所有基类
    elif hasattr(obj.__class__, "__bases__"):
        for base in obj.__class__.__bases__:
            if attr_name in base.__dict__:
                print(f"  3. 在基类{base}中找到")
                return base.__dict__[attr_name]

    print(f"  属性 '{attr_name}' 未找到")
    raise AttributeError(
        f"'{obj.__class__.__name__}' object has no attribute '{attr_name}'"
    )


# 演示属性查找
explain_attribute_lookup(alice, "name")  # 在实例字典中找到
explain_attribute_lookup(alice, "species")  # 在类字典中找到
explain_attribute_lookup(alice, "greet")  # 在类字典中找到方法


# 3. 动态修改对象
print("\n\n3. 动态添加、修改和删除属性")
print("-" * 40)

print(f"修改前 - alice.__dict__: {alice.__dict__}")

# 动态添加属性
alice.email = "alice@example.com"
alice.job = "Engineer"

print(f"添加属性后 - alice.__dict__: {alice.__dict__}")

# 修改属性
alice.age = 26
print(f"修改age后 - alice.__dict__: {alice.__dict__}")

# 删除属性
del alice.job
print(f"删除job后 - alice.__dict__: {alice.__dict__}")

# bob的字典不受影响
print(f"bob.__dict__ (未受影响): {bob.__dict__}")


# 4. 查看类字典内容
print("\n\n4. 类字典详细内容分析")
print("-" * 40)

print("Person.__dict__ 中的内容:")
for key, value in Person.__dict__.items():
    # 过滤掉特殊方法，只显示重要的
    if not key.startswith("__") or key in ["__init__", "__module__", "__doc__"]:
        value_type = type(value).__name__
        value_preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
        print(f"  {key:20} : {value_type:15} = {value_preview}")


# 5. 方法和函数的关系
print("\n\n5. 方法与绑定机制")
print("-" * 40)

# 直接从类字典中获取方法
greet_method = Person.__dict__["greet"]
print(f"Person.__dict__['greet']: {greet_method}")

# 通过实例访问方法（绑定方法）
alice_greet = alice.greet
print(f"alice.greet: {alice_greet}")

# 调用它们
print(f"\n调用 Person.greet(alice): {Person.greet(alice)}")
print(f"调用 alice.greet(): {alice.greet()}")


# 6. 继承和字典关系
print("\n\n6. 继承关系中的字典")
print("-" * 40)


class Student(Person):
    """继承自Person的子类"""

    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    def study(self):
        return f"{self.name} is studying."


# 创建Student实例
charlie = Student("Charlie", 20, "S12345")

print(f"charlie.__dict__: {charlie.__dict__}")
print(f"Student.__dict__ 键: {list(Student.__dict__.keys())}")

# 演示继承链查找
print(f"\n继承查找演示:")
explain_attribute_lookup(charlie, "name")  # 实例属性
explain_attribute_lookup(charlie, "study")  # 子类方法
explain_attribute_lookup(charlie, "species")  # 父类属性
explain_attribute_lookup(charlie, "greet")  # 父类方法


# 7. 内存地址和ID展示
print("\n\n7. 对象内存标识")
print("-" * 40)

print(f"alice对象ID: {id(alice)}")
print(f"bob对象ID: {id(bob)}")
print(f"Person类ID: {id(Person)}")
print(f"Student类ID: {id(Student)}")

print(f"\nalice.__class__ 是 Person? {alice.__class__ is Person}")
print(f"bob.__class__ 是 Person? {bob.__class__ is Person}")
print(f"charlie.__class__ 是 Student? {charlie.__class__ is Student}")


# 8. 使用getattr、setattr、hasattr操作属性
print("\n\n8. 使用属性访问函数")
print("-" * 40)

# 动态操作属性
setattr(bob, "hobby", "Swimming")
print(f"setattr后 bob.__dict__: {bob.__dict__}")

hobby = getattr(bob, "hobby", "No hobby")
print(f"getattr获取 bob.hobby: {hobby}")

print(f"hasattr检查 bob.email: {hasattr(bob, 'email')}")
print(f"hasattr检查 bob.hobby: {hasattr(bob, 'hobby')}")


# 9. 实际应用：遍历对象属性
print("\n\n9. 遍历和操作对象属性")
print("-" * 40)


def inspect_object(obj):
    """详细检查对象的所有属性"""
    print(f"\n检查对象: {obj}")
    print(f"类: {obj.__class__.__name__}")

    print("\n实例属性 (__dict__):")
    for key, value in obj.__dict__.items():
        print(f"  {key}: {value}")

    print("\n可访问的方法 (来自类):")
    for attr_name in dir(obj):
        if not attr_name.startswith("__"):
            attr = getattr(obj, attr_name)
            if callable(attr) and attr_name != "callable":
                print(f"  {attr_name}()")


inspect_object(charlie)


# 10. 性能考虑：大量实例的内存使用
print("\n\n10. 内存使用考虑")
print("-" * 40)

# 创建多个实例
print("创建1000个简单实例...")
instances = [Person(f"Person{i}", i % 80) for i in range(1000)]

# 计算总内存使用
total_size = sum(
    sys.getsizeof(inst.__dict__) for inst in instances[:10]
)  # 只计算前10个
avg_dict_size = sys.getsizeof(instances[0].__dict__)

print(f"每个实例字典大约大小: {avg_dict_size} 字节")
print(f"1000个实例字典约使用: {avg_dict_size * 1000 / 1024:.1f} KB")
print("\n注: 实际内存更大，因为每个字典项和对象本身也占内存")

print("\n" + "=" * 60)
print("示例结束 - Python对象本质上是'带类型的字典'")
print("=" * 60)


# 11. 扩展：展示描述符的简单实现
print("\n\n[扩展] 简单描述符示例")
print("-" * 40)


class ValidatedAttribute:
    """简单的描述符，用于属性验证"""

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype):
        print(f"描述符__get__: 获取{self.name}")
        return obj.__dict__.get(self.name, None)

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name}必须是字符串")
        print(f"描述符__set__: 设置{self.name} = {value}")
        obj.__dict__[self.name] = value


class User:
    """使用描述符的类"""

    username = ValidatedAttribute("username")
    email = ValidatedAttribute("email")

    def __init__(self, username, email):
        self.username = username
        self.email = email


print("\n创建User实例:")
user = User("john_doe", "john@example.com")
print(f"user.__dict__: {user.__dict__}")

print("\n通过描述符访问属性:")
print(f"user.username: {user.username}")

print("\n尝试设置错误类型:")
try:
    user.username = 123  # 会触发TypeError
except TypeError as e:
    print(f"错误: {e}")
