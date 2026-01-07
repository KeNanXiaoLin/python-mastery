"""
Python闭包与函数返回完整示例
展示闭包、高阶函数、函数返回和函数式编程模式
"""

print("=" * 80)
print("Python闭包与函数返回完整示例")
print("=" * 80)


# ============================================================================
# 第一部分：基础闭包演示
# ============================================================================
print("\n" + "=" * 80)
print("1. 基础闭包演示")
print("=" * 80)


def outer_function(x):
    """外部函数，返回内部函数（闭包）"""
    print(f"outer_function被调用: x = {x}")

    def inner_function(y):
        """内部函数，形成闭包"""
        print(f"inner_function被调用: x = {x}, y = {y}")
        return x + y  # 访问外部函数的变量x

    print(f"outer_function返回inner_function")
    return inner_function  # 返回内部函数


print("\n创建闭包:")
print("-" * 40)
closure1 = outer_function(10)  # 调用外部函数，返回内部函数
print(f"closure1 = {closure1}")
print(f"closure1.__name__ = {closure1.__name__}")

print("\n使用闭包:")
print("-" * 40)
result1 = closure1(5)  # 调用闭包，x=10, y=5
print(f"closure1(5) = {result1}")

result2 = closure1(15)  # 再次调用，x仍然是10
print(f"closure1(15) = {result2}")

print("\n创建另一个闭包:")
print("-" * 40)
closure2 = outer_function(100)  # 新的闭包，x=100
print(f"closure2(20) = {closure2(20)}")  # x=100, y=20

print("\n对比两个闭包:")
print("-" * 40)
print(f"closure1 is closure2? {closure1 is closure2}")
print(f"closure1.__closure__ = {closure1.__closure__}")
print(f"closure2.__closure__ = {closure2.__closure__}")

print("\n查看闭包捕获的变量:")
print("-" * 40)
if closure1.__closure__:
    for i, cell in enumerate(closure1.__closure__):
        print(f"  cell{i}: {cell}, contents = {cell.cell_contents}")

print("\n闭包与普通函数的区别:")
print("-" * 40)


def regular_func(y):
    """普通函数，没有闭包"""
    return 10 + y  # 硬编码10，不是从外部捕获


print(f"regular_func(5) = {regular_func(5)}")
print(f"hasattr(regular_func, '__closure__')? {hasattr(regular_func, '__closure__')}")
print(f"regular_func.__closure__ = {regular_func.__closure__}")

# ============================================================================
# 第二部分：闭包的智能捕获机制
# ============================================================================
print("\n\n" + "=" * 80)
print("2. 闭包的智能捕获机制")
print("=" * 80)


def smart_closure(a, b, c):
    """演示闭包只捕获实际使用的变量"""
    print(f"smart_closure被调用: a={a}, b={b}, c={c}")

    unused = a * 10  # 这个变量不会被使用

    def inner1():
        """只使用a"""
        return f"inner1: a={a}"

    def inner2():
        """使用a和b"""
        return f"inner2: a={a}, b={b}, sum={a+b}"

    def inner3():
        """使用所有变量"""
        return f"inner3: a={a}, b={b}, c={c}, total={a+b+c}"

    def inner4():
        """只使用中间计算结果"""
        result = a + b
        return f"inner4: result={result}"

    return inner1, inner2, inner3, inner4


print("\n创建智能闭包:")
print("-" * 40)
closures = smart_closure(1, 2, 3)
inner1, inner2, inner3, inner4 = closures

print("\n调用inner1 (只使用a):")
print(f"inner1() = {inner1()}")
print(f"inner1.__closure__ 长度: {len(inner1.__closure__)}")
print(f"捕获的变量: {[cell.cell_contents for cell in inner1.__closure__]}")

print("\n调用inner2 (使用a和b):")
print(f"inner2() = {inner2()}")
print(f"inner2.__closure__ 长度: {len(inner2.__closure__)}")
print(f"捕获的变量: {[cell.cell_contents for cell in inner2.__closure__]}")

print("\n调用inner3 (使用a, b, c):")
print(f"inner3() = {inner3()}")
print(f"inner3.__closure__ 长度: {len(inner3.__closure__)}")

print("\n调用inner4 (只使用中间结果):")
print(f"inner4() = {inner4()}")
print(f"inner4.__closure__ 长度: {len(inner4.__closure__)}")
print(f"inner4捕获了a和b吗? {len(inner4.__closure__) == 1}")

# ============================================================================
# 第三部分：可变闭包与状态保持
# ============================================================================
print("\n\n" + "=" * 80)
print("3. 可变闭包与状态保持")
print("=" * 80)

print("\n计数器闭包 (使用nonlocal):")
print("-" * 40)


def make_counter(start=0):
    """创建计数器闭包"""
    count = start  # 闭包变量

    def counter():
        """计数器函数"""
        nonlocal count  # 声明count是闭包变量，可以修改
        count += 1
        return count

    def get_count():
        """只读访问"""
        return count

    def reset(new_start=0):
        """重置计数器"""
        nonlocal count
        count = new_start
        return count

    return counter, get_count, reset


# 创建计数器
increment, get_value, reset_counter = make_counter(10)

print("初始计数器:")
print(f"get_value() = {get_value()}")
print(f"increment() = {increment()}")
print(f"increment() = {increment()}")
print(f"increment() = {increment()}")
print(f"当前值: get_value() = {get_value()}")

print("\n重置计数器:")
print(f"reset_counter(100) = {reset_counter(100)}")
print(f"increment() = {increment()}")

print("\n创建多个独立计数器:")
print("-" * 40)
counterA, _, _ = make_counter(0)
counterB, _, _ = make_counter(100)

print(f"counterA(): {counterA()}, {counterA()}, {counterA()}")
print(f"counterB(): {counterB()}, {counterB()}")
print("两个计数器状态独立!")

print("\n不使用nonlocal的问题:")
print("-" * 40)


def broken_counter(start=0):
    """有问题的计数器 (没有nonlocal)"""
    count = start

    def counter():
        # 错误: 没有声明nonlocal，会创建局部变量
        count = count + 1  # 这会报错!
        return count

    return counter


try:
    broken = broken_counter()
    broken()
except UnboundLocalError as e:
    print(f"错误: {e}")
    print("原因: 没有使用nonlocal声明，Python认为count是局部变量")

print("\n闭包实现缓存:")
print("-" * 40)


def make_cached_function(func):
    """创建带缓存的函数闭包"""
    cache = {}  # 缓存字典，闭包变量

    def cached_func(*args):
        """带缓存的函数"""
        if args in cache:
            print(f"  缓存命中: {args} -> {cache[args]}")
            return cache[args]

        print(f"  计算新值: {args}")
        result = func(*args)
        cache[args] = result
        return result

    def cache_info():
        """获取缓存信息"""
        return {"size": len(cache), "keys": list(cache.keys())}

    def clear_cache():
        """清除缓存"""
        cache.clear()
        return "缓存已清除"

    return cached_func, cache_info, clear_cache


# 创建昂贵计算的缓存版本
def expensive_computation(n):
    """模拟昂贵计算"""
    print(f"  执行昂贵计算: {n}")
    import time

    time.sleep(0.1)  # 模拟耗时
    return n * n


cached_square, get_info, clear = make_cached_function(expensive_computation)

print("\n第一次调用(计算):")
print(f"cached_square(5) = {cached_square(5)}")

print("\n第二次调用(从缓存):")
print(f"cached_square(5) = {cached_square(5)}")

print("\n新参数(计算):")
print(f"cached_square(10) = {cached_square(10)}")

print("\n缓存信息:")
info = get_info()
print(f"缓存大小: {info['size']}")
print(f"缓存键: {info['keys']}")

print("\n清除缓存:")
print(clear())
print(f"清除后缓存大小: {get_info()['size']}")

# ============================================================================
# 第四部分：函数工厂模式
# ============================================================================
print("\n\n" + "=" * 80)
print("4. 函数工厂模式")
print("=" * 80)

print("\n数学运算工厂:")
print("-" * 40)


def math_operation_factory(operation):
    """根据操作创建不同的数学函数"""

    if operation == "add":

        def add_func(a, b):
            return a + b

        return add_func

    elif operation == "multiply":

        def multiply_func(a, b):
            return a * b

        return multiply_func

    elif operation == "power":

        def power_func(a, b):
            return a**b

        return power_func

    else:

        def default_func(a, b):
            return f"未知操作: {operation}"

        return default_func


# 创建不同的数学函数
add = math_operation_factory("add")
multiply = math_operation_factory("multiply")
power = math_operation_factory("power")

print(f"add(3, 4) = {add(3, 4)}")
print(f"multiply(3, 4) = {multiply(3, 4)}")
print(f"power(3, 4) = {power(3, 4)}")

print("\n带参数的函数工厂:")
print("-" * 40)


def make_multiplier(factor):
    """创建乘以特定因子的函数"""

    def multiplier(x):
        return x * factor

    return multiplier


double = make_multiplier(2)
triple = make_multiplier(3)
times_ten = make_multiplier(10)

print(f"double(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")
print(f"times_ten(5) = {times_ten(5)}")

print("\n验证闭包捕获:")
print(f"double.__closure__[0].cell_contents = {double.__closure__[0].cell_contents}")
print(f"triple.__closure__[0].cell_contents = {triple.__closure__[0].cell_contents}")

print("\n函数组合工厂:")
print("-" * 40)


def compose_functions(f, g):
    """创建函数组合 (f ∘ g)(x) = f(g(x))"""

    def composed(x):
        return f(g(x))

    return composed


def add_one(x):
    return x + 1


def square(x):
    return x * x


# 创建组合函数
add_then_square = compose_functions(square, add_one)  # (x+1)²
square_then_add = compose_functions(add_one, square)  # x² + 1

print(f"add_then_square(2) = (2+1)² = {add_then_square(2)}")
print(f"square_then_add(2) = 2²+1 = {square_then_add(2)}")


# ============================================================================
# 第五部分：闭包的实际应用
# ============================================================================
print("\n\n" + "=" * 80)
print("5. 闭包的实际应用")
print("=" * 80)

print("\n1. 配置预设函数:")
print("-" * 40)


def make_greeting_template(greeting, punctuation):
    """创建特定问候语模板"""

    def greet(name):
        return f"{greeting}, {name}{punctuation}"

    return greet


hello_greet = make_greeting_template("Hello", "!")
hi_greet = make_greeting_template("Hi", ".")
formal_greet = make_greeting_template("Good day", ",")

print(f"hello_greet('Alice') = {hello_greet('Alice')}")
print(f"hi_greet('Bob') = {hi_greet('Bob')}")
print(f"formal_greet('Charlie') = {formal_greet('Charlie')}")

print("\n2. 事件处理器工厂:")
print("-" * 40)


def make_event_handler(event_type, threshold=0):
    """创建事件处理器"""

    def handler(data, callback=None):
        """处理事件"""
        print(f"处理 {event_type} 事件: {data}")

        if event_type == "click" and callback:
            callback(data)

        elif event_type == "value_change":
            if data > threshold:
                print(f"  值 {data} 超过阈值 {threshold}")

        elif event_type == "timer":
            print(f"  定时器触发: {data}ms")

    return handler


click_handler = make_event_handler("click")
value_handler = make_event_handler("value_change", threshold=100)
timer_handler = make_event_handler("timer")


def click_callback(data):
    print(f"  点击回调: {data}")


print("模拟事件处理:")
click_handler("按钮A", click_callback)
value_handler(150)
timer_handler(5000)

print("\n3. 装饰器作为闭包:")
print("-" * 40)


def timing_decorator(func):
    """计时装饰器（本质上是闭包）"""
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"函数 {func.__name__} 执行时间: {end - start:.6f}秒")
        return result

    return wrapper


@timing_decorator
def slow_function():
    """模拟慢函数"""
    import time

    time.sleep(0.5)
    return "完成"


print("调用装饰后的函数:")
result = slow_function()
print(f"结果: {result}")

print("\n手动创建装饰器（展示闭包本质）:")
print("-" * 40)


def manual_decorator():
    """手动创建装饰器效果"""

    def original_func():
        return "原始函数"

    decorated = timing_decorator(original_func)  # 应用装饰器
    print(f"装饰后的函数: {decorated}")
    return decorated()


manual_result = manual_decorator()
print(f"手动装饰结果: {manual_result}")


# ============================================================================
# 第六部分：闭包与对象的对比
# ============================================================================
print("\n\n" + "=" * 80)
print("6. 闭包与对象的对比")
print("=" * 80)

print("\n用闭包实现计数器:")
print("-" * 40)


def counter_closure(initial=0):
    """闭包实现的计数器"""
    count = initial

    def increment():
        nonlocal count
        count += 1
        return count

    def decrement():
        nonlocal count
        count -= 1
        return count

    def get():
        return count

    def reset(value=0):
        nonlocal count
        count = value
        return count

    # 返回方法字典
    return {"increment": increment, "decrement": decrement, "get": get, "reset": reset}


print("\n用类实现计数器:")
print("-" * 40)


class CounterClass:
    """类实现的计数器"""

    def __init__(self, initial=0):
        self.count = initial

    def increment(self):
        self.count += 1
        return self.count

    def decrement(self):
        self.count -= 1
        return self.count

    def get(self):
        return self.count

    def reset(self, value=0):
        self.count = value
        return self.count


print("\n使用对比:")
print("-" * 40)

# 使用闭包
closure_counter = counter_closure(10)
print("闭包计数器:")
print(f"  初始值: {closure_counter['get']()}")
print(f"  increment: {closure_counter['increment']()}")
print(f"  increment: {closure_counter['increment']()}")
print(f"  当前值: {closure_counter['get']()}")

# 使用类
class_counter = CounterClass(10)
print("\n类计数器:")
print(f"  初始值: {class_counter.get()}")
print(f"  increment: {class_counter.increment()}")
print(f"  increment: {class_counter.increment()}")
print(f"  当前值: {class_counter.get()}")

print("\n内存和性能考虑:")
print("-" * 40)
print("闭包优点:")
print("  1. 更轻量，不需要self参数")
print("  2. 变量完全私有，无法从外部访问")
print("  3. 创建速度快")
print("\n类优点:")
print("  1. 更容易理解和维护")
print("  2. 支持继承和多态")
print("  3. 更好的IDE支持")

print("\n" + "=" * 80)
print("闭包总结")
print("=" * 80)
print(
    """
关键要点:
1. 闭包 = 函数 + 捕获的环境变量
2. __closure__属性包含捕获的变量
3. 智能捕获: 只捕获实际使用的变量
4. nonlocal允许修改闭包变量
5. 闭包可以维护状态，类似于对象
6. 函数工厂: 根据参数动态创建函数
7. 实际应用: 缓存、装饰器、事件处理、配置预设

闭包 vs 对象:
- 闭包: 轻量级状态封装，适合简单场景
- 对象: 完整面向对象，适合复杂场景

记住: 装饰器、回调函数、延迟求值等都基于闭包机制!
"""
)
print("=" * 80)
