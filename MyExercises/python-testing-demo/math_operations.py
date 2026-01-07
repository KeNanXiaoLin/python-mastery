"""
数学运算函数模块
"""


def add(x, y):
    """
    将x和y相加。

    Args:
        x: 第一个参数
        y: 第二个参数

    Returns:
        两数之和

    Examples:
        >>> add(2, 3)
        5
        >>> add('hello', 'world')
        'helloworld'
    """
    return x + y


def divide(x, y):
    """
    除法运算

    Args:
        x: 被除数
        y: 除数

    Returns:
        商

    Raises:
        ZeroDivisionError: 除数为零
        TypeError: 参数类型错误
    """
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("参数必须是数字")

    if y == 0:
        raise ZeroDivisionError("除数不能为零")

    return x / y


def find_max(numbers):
    """
    查找列表中的最大值

    Args:
        numbers: 数字列表

    Returns:
        最大值

    Raises:
        ValueError: 列表为空
    """
    if not numbers:
        raise ValueError("列表不能为空")

    return max(numbers)


def multiply(x, y):
    """
    乘法运算

    Args:
        x: 第一个因数
        y: 第二个因数

    Returns:
        乘积

    Raises:
        TypeError: 参数类型错误
    """
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("参数必须是数字")

    return x * y
