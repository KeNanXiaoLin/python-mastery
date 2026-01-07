"""
测试运行脚本
"""

import unittest
import sys
import os


def run_all_tests():
    """运行所有测试"""
    print("=" * 80)
    print("运行Python单元测试")
    print("=" * 80)

    # 添加当前目录到路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # 发现并运行所有测试
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")

    # 运行测试
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)

    # 打印摘要
    print("\n" + "=" * 80)
    print("测试结果摘要:")
    print(f"  运行测试数: {result.testsRun}")
    print(f"  失败数: {len(result.failures)}")
    print(f"  错误数: {len(result.errors)}")
    print(f"  跳过数: {len(result.skipped)}")
    print("=" * 80)

    # 返回退出码
    return 0 if result.wasSuccessful() else 1


def run_specific_test(test_name):
    """运行特定测试"""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromName(test_name)

    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="运行单元测试")
    parser.add_argument(
        "--test", help="运行特定测试（例如：tests.test_bank_account.TestBankAccount）"
    )

    args = parser.parse_args()

    if args.test:
        exit_code = run_specific_test(args.test)
    else:
        exit_code = run_all_tests()

    sys.exit(exit_code)
