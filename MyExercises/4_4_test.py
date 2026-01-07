"""
Python属性访问拦截完整示例
展示__getattribute__, __getattr__, __setattr__, __delattr__的工作原理
"""

print("=" * 80)
print("Python属性访问拦截完整示例")
print("=" * 80)


# ============================================================================
# 第一部分：基础属性访问方法
# ============================================================================
print("\n" + "=" * 80)
print("1. 基础属性访问方法演示")
print("=" * 80)


class AttributeLogger:
    """记录所有属性访问的类"""

    def __init__(self, name):
        print(f"AttributeLogger.__init__: name={name}")
        # 使用对象字典直接设置，避免触发__setattr__
        self.__dict__["name"] = name
        self.__dict__["_data"] = {}

    def __getattribute__(self, name):
        """拦截所有属性读取"""
        print(f"__getattribute__ 被调用: 读取属性 '{name}'")

        # 必须通过object.__getattribute__访问父类实现，避免递归
        try:
            # 注意：不能使用 self.name 或 super().__getattribute__，会递归！
            value = object.__getattribute__(self, name)
            print(f"  __getattribute__: 找到属性 '{name}' = {value}")
            return value
        except AttributeError:
            print(f"  __getattribute__: 属性 '{name}' 未找到，交给 __getattr__")
            # 触发 __getattr__
            raise

    def __getattr__(self, name):
        """当属性未找到时调用"""
        print(f"__getattr__ 被调用: 属性 '{name}' 未找到")

        # 提供默认值
        if name.startswith("default_"):
            default_value = f"默认值: {name[8:]}"
            print(f"  __getattr__: 返回默认值 '{default_value}'")
            return default_value

        # 模拟动态属性
        if name in self._data:
            print(f"  __getattr__: 从_data中找到 '{name}' = {self._data[name]}")
            return self._data[name]

        print(f"  __getattr__: 抛出AttributeError")
        raise AttributeError(f"'{self.__class__.__name__}' 对象没有属性 '{name}'")

    def __setattr__(self, name, value):
        """拦截所有属性设置"""
        print(f"__setattr__ 被调用: 设置属性 '{name}' = {value}")

        # 特殊处理：保护某些属性
        if name == "secret" and not hasattr(self, "_has_secret_permission"):
            print(f"  __setattr__: 拒绝设置保护属性 'secret'")
            raise AttributeError("没有权限设置 'secret' 属性")

        # 验证规则
        if name == "age" and not isinstance(value, (int, float)):
            print(f"  __setattr__: 年龄必须是数字")
            raise TypeError("年龄必须是数字")

        # 记录所有设置操作
        if not hasattr(self, "_set_history"):
            object.__setattr__(self, "_set_history", [])

        self._set_history.append((name, value))
        print(f"  __setattr__: 已记录设置操作，共 {len(self._set_history)} 条记录")

        # 使用object.__setattr__避免递归
        object.__setattr__(self, name, value)
        print(f"  __setattr__: 属性 '{name}' 已设置")

    def __delattr__(self, name):
        """拦截所有属性删除"""
        print(f"__delattr__ 被调用: 删除属性 '{name}'")

        # 保护某些属性不被删除
        if name in ["name", "_set_history"]:
            print(f"  __delattr__: 拒绝删除保护属性 '{name}'")
            raise AttributeError(f"不能删除保护属性 '{name}'")

        # 记录删除操作
        if hasattr(self, "_delete_history"):
            self._delete_history.append(name)
        else:
            object.__setattr__(self, "_delete_history", [name])

        print(f"  __delattr__: 已记录删除操作")

        # 使用object.__delattr__删除
        object.__delattr__(self, name)
        print(f"  __delattr__: 属性 '{name}' 已删除")

    def get_history(self):
        """获取属性操作历史"""
        return {
            "set_history": getattr(self, "_set_history", []),
            "delete_history": getattr(self, "_delete_history", []),
        }


print("\n创建AttributeLogger实例:")
print("-" * 40)
logger = AttributeLogger("测试对象")

print("\n1. 读取已存在的属性:")
print("-" * 40)
print(f"logger.name = {logger.name}")

print("\n2. 读取不存在的属性:")
print("-" * 40)
try:
    print(f"logger.nonexistent = {logger.nonexistent}")
except AttributeError as e:
    print(f"错误: {e}")

print("\n3. 读取默认属性:")
print("-" * 40)
print(f"logger.default_color = {logger.default_color}")

print("\n4. 设置属性:")
print("-" * 40)
logger.age = 25
logger.email = "test@example.com"

print("\n5. 设置保护属性:")
print("-" * 40)
try:
    logger.secret = "confidential"
except AttributeError as e:
    print(f"错误: {e}")

print("\n6. 设置无效类型:")
print("-" * 40)
try:
    logger.age = "不是数字"
except TypeError as e:
    print(f"错误: {e}")

print("\n7. 删除属性:")
print("-" * 40)
logger.temp = "临时数据"
print(f"删除前: hasattr(logger, 'temp') = {hasattr(logger, 'temp')}")
del logger.temp
print(f"删除后: hasattr(logger, 'temp') = {hasattr(logger, 'temp')}")

print("\n8. 删除保护属性:")
print("-" * 40)
try:
    del logger.name
except AttributeError as e:
    print(f"错误: {e}")

print("\n9. 查看操作历史:")
print("-" * 40)
history = logger.get_history()
print(f"设置历史: {history['set_history']}")
print(f"删除历史: {history['delete_history']}")


# ============================================================================
# 第二部分：代理模式实现
# ============================================================================
print("\n\n" + "=" * 80)
print("2. 代理模式实现")
print("=" * 80)


class Circle:
    """被代理的原始类"""

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math

        return math.pi * self.radius**2

    def circumference(self):
        import math

        return 2 * math.pi * self.radius

    def __str__(self):
        return f"Circle(radius={self.radius})"

    def __repr__(self):
        return self.__str__()


class LoggingProxy:
    """带日志的代理类"""

    def __init__(self, obj):
        print(f"LoggingProxy.__init__: 创建代理包装 {obj}")
        # 直接设置内部对象，避免触发__setattr__
        self.__dict__["_obj"] = obj
        self.__dict__["_access_log"] = []

    def __getattr__(self, name):
        """拦截所有未找到的属性"""
        print(f"LoggingProxy.__getattr__: 访问属性 '{name}'")

        # 记录访问
        self._access_log.append(
            {"type": "getattr", "name": name, "timestamp": self._current_time()}
        )

        # 转发到实际对象
        try:
            value = getattr(self._obj, name)
            print(f"  LoggingProxy: 成功获取属性 '{name}' = {value}")
            return value
        except AttributeError:
            print(f"  LoggingProxy: 原始对象没有属性 '{name}'")
            raise

    def __setattr__(self, name, value):
        """拦截属性设置"""
        if name in ["_obj", "_access_log"]:
            # 直接设置内部属性
            object.__setattr__(self, name, value)
            return

        print(f"LoggingProxy.__setattr__: 设置属性 '{name}' = {value}")

        # 记录设置
        if hasattr(self, "_access_log"):
            self._access_log.append(
                {
                    "type": "setattr",
                    "name": name,
                    "value": value,
                    "timestamp": self._current_time(),
                }
            )

        # 转发到实际对象
        setattr(self._obj, name, value)
        print(f"  LoggingProxy: 已转发设置到原始对象")

    def __delattr__(self, name):
        """拦截属性删除"""
        print(f"LoggingProxy.__delattr__: 删除属性 '{name}'")

        # 记录删除
        self._access_log.append(
            {"type": "delattr", "name": name, "timestamp": self._current_time()}
        )

        # 转发到实际对象
        delattr(self._obj, name)
        print(f"  LoggingProxy: 已转发删除到原始对象")

    def _current_time(self):
        """获取当前时间字符串"""
        import datetime

        return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

    def get_access_log(self):
        """获取访问日志"""
        return self._access_log

    def __str__(self):
        return f"LoggingProxy({self._obj})"

    def __repr__(self):
        return self.__str__()


print("\n创建原始对象和代理:")
print("-" * 40)
circle = Circle(5.0)
print(f"原始对象: {circle}")
proxy = LoggingProxy(circle)
print(f"代理对象: {proxy}")

print("\n通过代理访问属性:")
print("-" * 40)
print(f"proxy.radius = {proxy.radius}")
print(f"proxy.area() = {proxy.area():.2f}")
print(f"proxy.circumference() = {proxy.circumference():.2f}")

print("\n通过代理修改属性:")
print("-" * 40)
proxy.radius = 7.0
print(f"修改后 proxy.area() = {proxy.area():.2f}")

print("\n查看访问日志:")
print("-" * 40)
log = proxy.get_access_log()
for entry in log:
    print(f"  {entry['timestamp']} - {entry['type']:8} - {entry['name']}", end="")
    if "value" in entry:
        print(f" = {entry['value']}")
    else:
        print()


# ============================================================================
# 第三部分：委托模式（作为继承的替代）
# ============================================================================
print("\n\n" + "=" * 80)
print("3. 委托模式实现")
print("=" * 80)


class FileReader:
    """文件读取器（被委托的类）"""

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        return f"从 {self.filename} 读取内容"

    def read_lines(self):
        return [f"{self.filename} 行 {i}" for i in range(1, 4)]

    def __len__(self):
        return len(self.read())

    def __getitem__(self, index):
        lines = self.read_lines()
        return lines[index]


class CachingFileHandler:
    """带缓存的文件处理器（使用委托）"""

    def __init__(self, filename):
        print(f"CachingFileHandler.__init__: filename={filename}")
        self._reader = FileReader(filename)  # 持有被委托对象
        self._cache = {}

    # 显式定义需要特殊处理的方法
    def __len__(self):
        """必须显式委托特殊方法"""
        print("CachingFileHandler.__len__: 显式委托")
        return len(self._reader)

    def __getitem__(self, index):
        """必须显式委托特殊方法"""
        print(f"CachingFileHandler.__getitem__: index={index}")

        # 实现缓存
        cache_key = f"item_{index}"
        if cache_key in self._cache:
            print(f"  从缓存获取: {cache_key}")
            return self._cache[cache_key]

        value = self._reader[index]
        self._cache[cache_key] = value
        print(f"  缓存新值: {cache_key} = {value}")
        return value

    # 普通方法通过__getattr__自动委托
    def __getattr__(self, name):
        """自动委托普通方法"""
        print(f"CachingFileHandler.__getattr__: 委托方法 '{name}'")

        if name.startswith("_"):
            raise AttributeError(f"不能访问私有属性 '{name}'")

        # 获取被委托对象的方法
        attr = getattr(self._reader, name)

        # 如果是可调用方法，包装它
        if callable(attr):

            def wrapper(*args, **kwargs):
                print(f"  调用委托方法: {name}{args}")
                # 可以在这里添加缓存、日志等逻辑
                return attr(*args, **kwargs)

            return wrapper
        else:
            # 如果是属性，直接返回
            return attr

    def clear_cache(self):
        """清除缓存（扩展功能）"""
        print("清除缓存")
        self._cache.clear()
        return len(self._cache)

    def get_cache_info(self):
        """获取缓存信息（扩展功能）"""
        return {"size": len(self._cache), "keys": list(self._cache.keys())}


print("\n创建CachingFileHandler实例:")
print("-" * 40)
handler = CachingFileHandler("data.txt")

print("\n1. 调用委托的普通方法:")
print("-" * 40)
print(f"handler.read() = {handler.read()}")
print(f"handler.read_lines() = {handler.read_lines()}")

print("\n2. 调用特殊方法（必须显式委托）:")
print("-" * 40)
print(f"len(handler) = {len(handler)}")
print(f"handler[0] = {handler[0]}")
print(f"handler[1] = {handler[1]}")  # 应该从缓存获取
print(f"handler[0] = {handler[0]}")  # 应该从缓存获取

print("\n3. 调用扩展方法:")
print("-" * 40)
cache_info = handler.get_cache_info()
print(f"缓存信息: {cache_info}")
handler.clear_cache()
print(f"清空后缓存大小: {handler.get_cache_info()['size']}")

print("\n4. 验证特殊方法委托限制:")
print("-" * 40)
print("__getattr__ 不处理特殊方法，必须显式委托")
print(f"handler.__len__ 是显式定义的: {hasattr(handler, '__len__')}")


# ============================================================================
# 第四部分：动态属性生成
# ============================================================================
print("\n\n" + "=" * 80)
print("4. 动态属性生成")
print("=" * 80)


class DynamicAttributes:
    """动态生成属性的类"""

    def __init__(self):
        self._prefix = "attr_"
        self._counter = 0
        self._dynamic_values = {}

    def __getattr__(self, name):
        """动态生成属性"""
        print(f"DynamicAttributes.__getattr__: 请求属性 '{name}'")

        # 动态生成属性
        if name.startswith(self._prefix):
            # 提取编号
            try:
                num = int(name[len(self._prefix) :])
                value = f"动态属性值 #{num}"
                print(f"  生成动态属性: {name} = {value}")

                # 缓存生成的值
                self._dynamic_values[name] = value
                return value
            except ValueError:
                pass

        # 计算属性
        if name.startswith("calc_"):
            operation = name[5:]
            if operation == "square":
                if hasattr(self, "base"):
                    result = self.base**2
                    print(f"  计算平方: {self.base}² = {result}")
                    return result

        # 惰性加载属性
        if name == "expensive_data":
            if "_expensive_data" not in self.__dict__:
                print("  执行昂贵计算...")
                import time

                time.sleep(0.1)  # 模拟计算
                self.__dict__["_expensive_data"] = [i**2 for i in range(10)]
                print(f"  计算完成，结果已缓存")
            return self.__dict__["_expensive_data"]

        raise AttributeError(f"没有属性 '{name}'")

    def __setattr__(self, name, value):
        """拦截设置，允许特殊处理"""
        if name == "base" and value < 0:
            print(f"  拒绝设置负基数")
            raise ValueError("基数不能为负数")

        print(f"DynamicAttributes.__setattr__: 设置 {name} = {value}")
        object.__setattr__(self, name, value)

    def list_dynamic_attributes(self):
        """列出所有动态生成的属性"""
        return list(self._dynamic_values.keys())


print("\n创建DynamicAttributes实例:")
print("-" * 40)
dyn = DynamicAttributes()

print("\n1. 访问动态属性:")
print("-" * 40)
print(f"dyn.attr_1 = {dyn.attr_1}")
print(f"dyn.attr_5 = {dyn.attr_5}")
print(f"dyn.attr_10 = {dyn.attr_10}")

print("\n2. 计算属性:")
print("-" * 40)
dyn.base = 5
print(f"dyn.calc_square = {dyn.calc_square}")

print("\n3. 惰性加载:")
print("-" * 40)
print(f"第一次访问 expensive_data: {dyn.expensive_data[:3]}...")
print(f"第二次访问（应该从缓存）: {dyn.expensive_data[:3]}...")

print("\n4. 验证设置拦截:")
print("-" * 40)
try:
    dyn.base = -5
except ValueError as e:
    print(f"错误: {e}")

print("\n5. 列出动态属性:")
print("-" * 40)
print(f"动态属性列表: {dyn.list_dynamic_attributes()}")


# ============================================================================
# 第五部分：访问控制（权限系统）
# ============================================================================
print("\n\n" + "=" * 80)
print("5. 访问控制（权限系统）")
print("=" * 80)


class SecureObject:
    """基于角色的访问控制"""

    ROLES = {
        "admin": ["read", "write", "delete"],
        "user": ["read", "write"],
        "guest": ["read"],
    }

    def __init__(self, data, role="guest"):
        self._data = data
        self._role = role
        self._audit_log = []

    def __getattribute__(self, name):
        """拦截所有访问"""
        # 允许访问内部属性
        if name.startswith("_"):
            return object.__getattribute__(self, name)

        # 检查权限
        if not self._check_permission("read", name):
            print(f"权限拒绝: {self._role} 角色不能读取 '{name}'")
            raise AttributeError(f"没有读取 '{name}' 的权限")

        print(f"允许读取: {self._role} -> '{name}'")
        self._audit("read", name)
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        """拦截所有设置"""
        # 允许设置内部属性
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return

        # 检查权限
        if not self._check_permission("write", name):
            print(f"权限拒绝: {self._role} 角色不能设置 '{name}'")
            raise AttributeError(f"没有设置 '{name}' 的权限")

        print(f"允许设置: {self._role} -> '{name}' = {value}")
        self._audit("write", name, value)
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        """拦截所有删除"""
        # 检查权限
        if not self._check_permission("delete", name):
            print(f"权限拒绝: {self._role} 角色不能删除 '{name}'")
            raise AttributeError(f"没有删除 '{name}' 的权限")

        print(f"允许删除: {self._role} -> '{name}'")
        self._audit("delete", name)
        object.__delattr__(self, name)

    def _check_permission(self, action, attribute):
        """检查权限"""
        # 使用object.__getattribute__直接访问，避免递归
        roles = object.__getattribute__(self.__class__, "ROLES")
        current_role = object.__getattribute__(self, "_role")
        allowed_actions = roles.get(current_role, [])
        return action in allowed_actions

    def _audit(self, action, attribute, value=None):
        """记录审计日志"""
        import datetime

        entry = {
            "timestamp": datetime.datetime.now(),
            "role": self._role,
            "action": action,
            "attribute": attribute,
            "value": value,
        }
        self._audit_log.append(entry)

    def get_audit_log(self):
        """获取审计日志"""
        return self._audit_log

    def change_role(self, new_role):
        """修改角色"""
        old_role = self._role
        self._role = new_role
        print(f"角色变更: {old_role} -> {new_role}")
        self._audit("role_change", None, f"{old_role}->{new_role}")


print("\n创建不同角色的对象:")
print("-" * 40)
# 创建admin对象
admin_obj = SecureObject({"id": 1, "name": "Admin Data"}, role="admin")
print(f"admin_obj._data = {admin_obj._data}")

# 创建user对象
user_obj = SecureObject({"id": 2, "name": "User Data"}, role="user")

# 创建guest对象
guest_obj = SecureObject({"id": 3, "name": "Guest Data"}, role="guest")

print("\n1. admin角色测试:")
print("-" * 40)
admin_obj.public_field = "公共数据"
del admin_obj.public_field

print("\n2. user角色测试:")
print("-" * 40)
user_obj.public_field = "用户数据"
try:
    del user_obj.public_field  # user不能删除
except AttributeError as e:
    print(f"错误: {e}")

print("\n3. guest角色测试:")
print("-" * 40)
try:
    guest_obj.public_field = "访客数据"  # guest不能写
except AttributeError as e:
    print(f"错误: {e}")

print(f"\nguest_obj 可以读取: guest_obj._data = {guest_obj._data}")

print("\n4. 角色变更测试:")
print("-" * 40)
guest_obj.change_role("user")
guest_obj.public_field = "现在可以写了"

print("\n5. 审计日志:")
print("-" * 40)
audit_log = guest_obj.get_audit_log()
for entry in audit_log[-3:]:  # 显示最后3条
    print(
        f"  {entry['timestamp'].strftime('%H:%M:%S')} "
        f"[{entry['role']}] {entry['action']} {entry['attribute']}"
    )
exit()
print("\n" + "=" * 80)
print("属性访问拦截总结")
print("=" * 80)
print(
    """
关键要点:
1. __getattribute__: 拦截所有属性读取，必须小心递归
2. __getattr__: 只在常规查找失败时调用，是安全网
3. __setattr__: 拦截所有属性设置，必须处理实际存储
4. __delattr__: 拦截所有属性删除
5. 代理模式: 拦截+转发，创建透明包装
6. 委托模式: 作为继承的替代，更灵活
7. 特殊方法限制: __getattr__不处理__len__等特殊方法
8. 实际应用: 日志、缓存、验证、权限控制、动态属性

最佳实践:
1. 总是通过object.__getattribute__等避免递归
2. __getattr__应抛出AttributeError，而不是返回None
3. __setattr__必须调用父类或object.__setattr__来存储
4. 对频繁访问的属性考虑缓存，避免性能问题
"""
)
print("=" * 80)
