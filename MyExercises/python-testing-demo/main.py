"""
Python测试与调试主演示程序
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bank_account import BankAccount
from math_operations import add, divide, find_max

print("=" * 80)
print("Python测试与调试演示")
print("=" * 80)


def demonstrate_bank_account():
    """演示银行账户功能"""
    print("\n" + "=" * 40)
    print("银行账户演示")
    print("=" * 40)

    try:
        account = BankAccount(1000)
        print(f"账户创建成功，初始余额: {account.get_balance()}")

        account.deposit(500)
        print(f"存款成功，当前余额: {account.get_balance()}")

        account.withdraw(200)
        print(f"取款成功，当前余额: {account.get_balance()}")

        # 创建第二个账户进行转账
        account2 = BankAccount(500)
        account.transfer(300, account2)
        print(f"转账成功，账户1余额: {account.get_balance()}")
        print(f"账户2余额: {account2.get_balance()}")

    except Exception as e:
        print(f"错误: {e}")


def demonstrate_math_operations():
    """演示数学运算功能"""
    print("\n" + "=" * 40)
    print("数学运算演示")
    print("=" * 40)

    print(f"add(2, 3) = {add(2, 3)}")
    print(f"add('hello', 'world') = {add('hello', 'world')}")

    print(f"divide(10, 2) = {divide(10, 2)}")

    try:
        print(f"divide(10, 0) = ...")
        divide(10, 0)
    except ZeroDivisionError as e:
        print(f"  错误: {e}")

    print(f"find_max([1, 5, 3, 9, 2]) = {find_max([1, 5, 3, 9, 2])}")


def demonstrate_assertions():
    """演示断言功能"""
    print("\n" + "=" * 40)
    print("断言演示")
    print("=" * 40)

    print("1. 正常的断言:")
    x = 5
    assert x > 0, "x应该是正数"
    print("  断言通过")

    print("\n2. 失败的断言:")
    try:
        y = -1
        assert y > 0, "y应该是正数"
    except AssertionError as e:
        print(f"  断言失败: {e}")

    print("\n3. 断言在调试和生产模式下的区别:")
    print(f"  当前调试模式: {__debug__}")
    print("  使用 'python -O main.py' 运行可以禁用断言")


if __name__ == "__main__":
    demonstrate_bank_account()
    demonstrate_math_operations()
    demonstrate_assertions()

    print("\n" + "=" * 80)
    print("演示完成")
    print("=" * 80)
    print("\n运行测试:")
    print("  python run_tests.py          # 运行所有测试")
    print("  python -m pytest tests/      # 使用pytest运行测试")
    print("  python -m unittest discover tests  # 使用unittest发现测试")
