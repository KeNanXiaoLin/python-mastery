"""
高级测试技巧演示
"""

import unittest
import unittest.mock as mock
import datetime
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestWithClassFixtures(unittest.TestCase):
    """演示类级别的fixture"""

    @classmethod
    def setUpClass(cls):
        """整个测试类前运行一次"""
        print("  setUpClass: 准备测试数据...")
        cls.shared_data = [1, 2, 3, 4, 5]
        cls.db_connection = "模拟数据库连接"

    @classmethod
    def tearDownClass(cls):
        """整个测试类后运行一次"""
        print("  tearDownClass: 清理资源...")
        cls.db_connection = None

    def test_data_access(self):
        """测试数据访问"""
        self.assertEqual(len(self.shared_data), 5)
        self.assertIn(3, self.shared_data)

    def test_db_connection(self):
        """测试数据库连接"""
        self.assertEqual(self.db_connection, "模拟数据库连接")


class TimeSensitiveFunction:
    """依赖于当前时间的函数"""

    def get_current_hour(self):
        """获取当前小时"""
        return datetime.datetime.now().hour

    def is_business_hours(self):
        """判断是否是工作时间"""
        hour = self.get_current_hour()
        return 9 <= hour < 17


class TestTimeSensitive(unittest.TestCase):
    """测试时间敏感函数"""

    def test_is_business_hours_morning(self):
        """测试上午（工作时间）"""
        # 创建测试对象
        obj = TimeSensitiveFunction()

        # 模拟datetime.datetime.now()返回特定时间
        mock_now = mock.Mock()
        mock_now.hour = 10  # 上午10点

        with mock.patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_now

            # 现在应该是工作时间
            self.assertTrue(obj.is_business_hours())

    def test_is_business_hours_evening(self):
        """测试晚上（非工作时间）"""
        obj = TimeSensitiveFunction()

        mock_now = mock.Mock()
        mock_now.hour = 20  # 晚上8点

        with mock.patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_now

            # 现在应该不是工作时间
            self.assertFalse(obj.is_business_hours())

    def test_mock_function(self):
        """模拟函数调用"""
        # 创建模拟对象
        mock_func = mock.Mock()
        mock_func.return_value = 42

        # 调用模拟函数
        result = mock_func()
        self.assertEqual(result, 42)

        # 验证函数被调用
        mock_func.assert_called_once()

        # 验证函数调用参数
        mock_func.reset_mock()
        mock_func(1, 2, 3, key="value")
        mock_func.assert_called_with(1, 2, 3, key="value")


class TestParameterized(unittest.TestCase):
    """手动参数化测试"""

    # 测试数据
    test_cases = [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (10, -5, 5),
    ]

    def test_add_multiple_cases(self):
        """测试多个用例"""
        from math_operations import add

        for a, b, expected in self.test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = add(a, b)
                self.assertEqual(
                    result,
                    expected,
                    f"add({a}, {b}) 应该返回 {expected}，但返回了 {result}",
                )


class TestExceptionMessages(unittest.TestCase):
    """测试异常消息"""

    def test_exception_message(self):
        """测试异常消息内容"""
        from math_operations import find_max

        with self.assertRaises(ValueError) as context:
            find_max([])

        # 验证异常消息
        self.assertEqual(str(context.exception), "列表不能为空")

        # 或者使用assertRaisesRegex
        with self.assertRaisesRegex(ValueError, "列表不能为空"):
            find_max([])


if __name__ == "__main__":
    unittest.main()
