"""
调试技巧测试
"""

import unittest
import logging
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def buggy_function(data):
    """有bug的函数"""
    result = []
    for item in data:
        # 假设这里有bug
        processed = item * 2  # 应该是 item ** 2

        # 可以在这里添加断点
        # import pdb; pdb.set_trace()

        result.append(processed)
    return result


def process_data_with_logging(data):
    """使用日志记录处理过程"""
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )

    logger = logging.getLogger(__name__)

    logger.debug(f"开始处理数据: {data}")

    if not data:
        logger.warning("收到空数据")
        return []

    result = []
    for i, item in enumerate(data):
        logger.debug(f"处理第 {i+1} 项: {item}")

        try:
            processed = item**2
            result.append(processed)
            logger.debug(f"处理结果: {processed}")
        except Exception as e:
            logger.error(f"处理项 {item} 时出错: {e}", exc_info=True)

    logger.info(f"数据处理完成，共处理 {len(result)} 项")
    return result


def complex_calculation(x, y):
    """复杂计算，使用断言帮助调试"""
    # 验证输入
    assert isinstance(x, (int, float)), f"x必须是数字，但得到 {type(x)}"
    assert isinstance(y, (int, float)), f"y必须是数字，但得到 {type(y)}"

    # 中间计算
    intermediate = x * y

    # 验证中间结果
    assert intermediate == x * y, f"乘法错误: {x} * {y} != {intermediate}"

    # 更多计算
    if x > 0:
        result = intermediate / x
    else:
        result = intermediate * (-1)

    # 验证最终结果
    assert not isinstance(result, complex), "结果不应该是复数"

    return result


def optimized_function(x, y):
    """使用__debug__优化调试代码"""
    result = x + y

    # 只在调试模式下检查
    if __debug__:
        # 昂贵的验证
        import math

        assert not math.isnan(result), "结果不能是NaN"
        assert not math.isinf(result), "结果不能是无穷大"

    return result


class TestDebugging(unittest.TestCase):
    """调试技巧测试"""

    def test_buggy_function(self):
        """测试有bug的函数"""
        result = buggy_function([1, 2, 3])
        self.assertEqual(result, [2, 4, 6])  # 注意：这是错误的，应该是 [1, 4, 9]

    def test_process_data_with_logging(self):
        """测试带日志的处理函数"""
        # 临时重定向日志输出
        import io
        import logging

        log_capture_string = io.StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.DEBUG)

        logger = logging.getLogger()
        logger.addHandler(ch)

        # 执行函数
        result = process_data_with_logging([1, 2, 3])

        # 检查结果
        self.assertEqual(result, [1, 4, 9])

        # 检查日志
        log_contents = log_capture_string.getvalue()
        self.assertIn("开始处理数据", log_contents)

        # 清理
        logger.removeHandler(ch)

    def test_complex_calculation(self):
        """测试复杂计算"""
        self.assertEqual(complex_calculation(6, 7), 7)
        self.assertEqual(complex_calculation(-1, 5), -5)

    def test_complex_calculation_assertion(self):
        """测试复杂计算的断言"""
        with self.assertRaises(AssertionError):
            complex_calculation("a", 5)

    def test_optimized_function(self):
        """测试优化函数"""
        self.assertEqual(optimized_function(3, 4), 7)

        # 测试调试模式
        print(f"调试模式: __debug__ = {__debug__}")


class TestPDBDebugging(unittest.TestCase):
    """测试pdb调试"""

    def test_pdb_available(self):
        """测试pdb是否可用"""
        try:
            import pdb

            self.assertTrue(True, "pdb模块可用")
        except ImportError:
            self.fail("pdb模块不可用")


if __name__ == "__main__":
    unittest.main()
