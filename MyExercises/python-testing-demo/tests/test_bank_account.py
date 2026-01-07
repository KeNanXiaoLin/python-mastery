"""
测试银行账户类
"""

import unittest
import sys
import os

# 添加父目录到路径，以便导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    """测试BankAccount类"""

    def setUp(self):
        """每个测试方法前运行"""
        self.account = BankAccount(1000)

    def tearDown(self):
        """每个测试方法后运行"""
        # 清理资源
        pass

    def test_initial_balance(self):
        """测试初始余额"""
        self.assertEqual(self.account.get_balance(), 1000)

    def test_deposit(self):
        """测试存款"""
        self.account.deposit(500)
        self.assertEqual(self.account.get_balance(), 1500)

    def test_deposit_invalid_amount(self):
        """测试无效存款金额"""
        with self.assertRaises(AssertionError):
            self.account.deposit(-100)

    def test_withdraw(self):
        """测试取款"""
        self.account.withdraw(300)
        self.assertEqual(self.account.get_balance(), 700)

    def test_withdraw_insufficient_funds(self):
        """测试余额不足"""
        with self.assertRaises(ValueError):
            self.account.withdraw(2000)

    def test_transaction_history(self):
        """测试交易记录"""
        self.account.deposit(500)
        self.account.withdraw(200)

        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 3)  # 开户 + 存款 + 取款

        # 验证最后一笔交易
        last_txn = transactions[-1]
        self.assertEqual(last_txn["description"], "取款")
        self.assertEqual(last_txn["amount"], -200)

    def test_transfer(self):
        """测试转账"""
        account2 = BankAccount(500)

        # 验证转账前余额
        self.assertEqual(self.account.get_balance(), 1000)
        self.assertEqual(account2.get_balance(), 500)

        # 执行转账
        self.account.transfer(300, account2)

        # 验证转账后余额
        self.assertEqual(self.account.get_balance(), 700)
        self.assertEqual(account2.get_balance(), 800)

    def test_transfer_invalid_target(self):
        """测试无效目标账户"""
        with self.assertRaises(AssertionError):
            self.account.transfer(100, "不是账户对象")

    def test_repr_method(self):
        """测试__repr__方法"""
        repr_str = repr(self.account)
        self.assertIn("BankAccount", repr_str)
        self.assertIn("balance=1000", repr_str)

    @unittest.skip("跳过这个测试，因为还在开发中")
    def test_skip_example(self):
        """示例：跳过的测试"""
        self.fail("这个测试不应该运行")


class TestBankAccountEdgeCases(unittest.TestCase):
    """测试银行账户边界情况"""

    def test_zero_initial_balance(self):
        """测试零初始余额"""
        account = BankAccount(0)
        self.assertEqual(account.get_balance(), 0)

    def test_large_deposit(self):
        """测试大额存款"""
        account = BankAccount(1000)
        account.deposit(1000000)
        self.assertEqual(account.get_balance(), 1001000)

    def test_consecutive_operations(self):
        """测试连续操作"""
        account = BankAccount(1000)
        account.deposit(500)
        account.withdraw(200)
        account.deposit(100)
        account.withdraw(50)

        self.assertEqual(account.get_balance(), 1350)
        self.assertEqual(len(account.get_transactions()), 5)


if __name__ == "__main__":
    unittest.main()
