"""
银行账户类，演示断言使用
"""


class BankAccount:
    """银行账户类，演示断言使用"""

    def __init__(self, initial_balance=0):
        """
        初始化账户

        Args:
            initial_balance: 初始余额，必须 >= 0
        """
        # 断言：验证程序不变量（内部条件）
        assert initial_balance >= 0, "初始余额不能为负数"

        self._balance = initial_balance
        self._transactions = []
        self._add_transaction("开户", initial_balance)

    def _add_transaction(self, description, amount):
        """添加交易记录（内部方法）"""
        # 断言：验证内部一致性
        assert hasattr(self, "_transactions"), "账户未正确初始化"
        self._transactions.append(
            {"description": description, "amount": amount, "balance": self._balance}
        )

    def deposit(self, amount):
        """
        存款

        Args:
            amount: 存款金额，必须 > 0
        Returns:
            新的余额
        """
        # 断言：验证前置条件（调用者责任）
        assert amount > 0, "存款金额必须大于0"
        assert isinstance(amount, (int, float)), "存款金额必须是数字"

        old_balance = self._balance
        self._balance += amount

        # 断言：验证后置条件（函数保证）
        assert self._balance == old_balance + amount, "余额计算错误"
        assert self._balance >= 0, "余额不能为负数"

        self._add_transaction("存款", amount)
        return self._balance

    def withdraw(self, amount):
        """
        取款

        Args:
            amount: 取款金额，必须 > 0
        Returns:
            新的余额
        Raises:
            ValueError: 余额不足
        """
        # 断言：验证参数
        assert amount > 0, "取款金额必须大于0"
        assert isinstance(amount, (int, float)), "取款金额必须是数字"

        # 用户错误使用异常，而不是断言
        if amount > self._balance:
            raise ValueError(f"余额不足。当前余额: {self._balance}")

        old_balance = self._balance
        self._balance -= amount

        # 断言：验证后置条件
        assert self._balance == old_balance - amount, "余额计算错误"
        assert self._balance >= 0, "余额不能为负数"

        self._add_transaction("取款", -amount)
        return self._balance

    def get_balance(self):
        """获取当前余额"""
        # 断言：验证内部状态一致性
        assert hasattr(self, "_balance"), "账户状态异常"
        return self._balance

    def get_transactions(self):
        """获取交易记录"""
        return self._transactions.copy()

    def transfer(self, amount, target_account):
        """
        转账给另一个账户

        Args:
            amount: 转账金额
            target_account: 目标账户
        """
        # 断言：验证参数类型
        assert isinstance(target_account, BankAccount), "目标账户必须是BankAccount实例"
        assert amount > 0, "转账金额必须大于0"

        # 验证不变量：转账前后总金额应保持不变
        total_before = self._balance + target_account._balance

        self.withdraw(amount)  # 可能引发异常
        target_account.deposit(amount)

        total_after = self._balance + target_account._balance

        # 断言：验证不变量
        assert total_after == total_before, "转账前后总金额不一致"
        self._add_transaction(f"转账给账户", -amount)

    def __repr__(self):
        return f"BankAccount(balance={self._balance})"
