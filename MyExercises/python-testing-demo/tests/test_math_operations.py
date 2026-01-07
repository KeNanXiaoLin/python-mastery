"""
测试数学运算函数
"""

import unittest
import sys
import os

# 添加父目录到路径，以便导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from math_operations import add, divide, find_max, multiply


class TestAdd(unittest.TestCase):
    """测试add函数"""

    def test_add_integers(self):
        """测试整数相加"""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_add_floats(self):
        """测试浮点数相加"""
        self.assertAlmostEqual(add(1.1, 2.2), 3.3, places=1)

    def test_add_strings(self):
        """测试字符串相加"""
        self.assertEqual(add("hello", "world"), "helloworld")

    def test_add_mixed_types(self):
        """测试混合类型（应该失败）"""
        with self.assertRaises(TypeError):
            add("5", 3)

    def test_add_large_numbers(self):
        """测试大数相加"""
        self.assertEqual(add(10**6, 10**6), 2 * 10**6)


class TestDivide(unittest.TestCase):
    """测试divide函数"""

    def test_divide_integers(self):
        """测试整数除法"""
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(9, 2), 4.5)

    def test_divide_by_zero(self):
        """测试除以零"""
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_divide_invalid_types(self):
        """测试无效类型"""
        with self.assertRaises(TypeError):
            divide("10", 2)
        with self.assertRaises(TypeError):
            divide(10, "2")

    def test_divide_negative(self):
        """测试负数除法"""
        self.assertEqual(divide(-10, 2), -5)
        self.assertEqual(divide(10, -2), -5)
        self.assertEqual(divide(-10, -2), 5)


class TestFindMax(unittest.TestCase):
    """测试find_max函数"""

    def test_find_max_normal(self):
        """测试正常情况"""
        self.assertEqual(find_max([1, 2, 3, 4, 5]), 5)
        self.assertEqual(find_max([-1, -2, -3]), -1)
        self.assertEqual(find_max([5]), 5)

    def test_find_max_empty_list(self):
        """测试空列表"""
        with self.assertRaises(ValueError):
            find_max([])

    def test_find_max_floats(self):
        """测试浮点数"""
        self.assertAlmostEqual(find_max([1.1, 2.2, 3.3]), 3.3, places=1)

    def test_find_max_duplicates(self):
        """测试重复值"""
        self.assertEqual(find_max([5, 5, 5]), 5)


class TestMultiply(unittest.TestCase):
    """测试multiply函数"""

    def test_multiply_integers(self):
        """测试整数乘法"""
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-3, 4), -12)
        self.assertEqual(multiply(0, 100), 0)

    def test_multiply_floats(self):
        """测试浮点数乘法"""
        self.assertAlmostEqual(multiply(2.5, 4.0), 10.0, places=1)

    def test_multiply_invalid_types(self):
        """测试无效类型"""
        with self.assertRaises(TypeError):
            multiply("3", 4)


if __name__ == "__main__":
    unittest.main()
