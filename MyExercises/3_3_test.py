class Player:
    """
    示例类：包含类属性、实例属性、@property、私有化属性的完整实现
    模拟游戏玩家，演示各类属性的定义、访问、修改规则
    """

    # -------------------------- 1. 类属性（所有实例共享） --------------------------
    # 类属性：玩家默认生命值（所有实例共享）
    DEFAULT_HP = 100
    # 类属性：统计创建的玩家总数（所有实例共享）
    player_count = 0

    # -------------------------- 2. 初始化方法（定义实例属性） --------------------------
    def __init__(self, name, x=0, y=0):
        # 实例属性：玩家名称（公开）
        self.name = name
        # 实例属性：坐标（私有化，仅内部访问）
        self._x = x  # 单下划线：约定私有（弱私有）
        self.__y = y  # 双下划线：名称改写（强私有）
        # 实例属性：生命值（通过@property封装）
        self._hp = Player.DEFAULT_HP

        # 修改类属性：玩家总数+1
        Player.player_count += 1

    # -------------------------- 3. @property 封装属性（受控访问） --------------------------
    # 3.1 只读属性：玩家坐标（组合_x和__y）
    @property
    def position(self):
        """只读属性：返回玩家坐标元组，无法直接修改"""
        return (self._x, self.__y)

    # 3.2 可读写属性：x坐标（带校验）
    @property
    def x(self):
        """获取x坐标（封装私有属性_x）"""
        return self._x

    @x.setter
    def x(self, value):
        """修改x坐标，添加数值校验"""
        if not isinstance(value, (int, float)):
            raise ValueError("x坐标必须是数字！")
        if value < 0 or value > 1000:
            raise ValueError("x坐标必须在0-1000之间！")
        self._x = value

    # 3.3 可读写属性：生命值（带逻辑）
    @property
    def hp(self):
        """获取生命值，确保不会为负数"""
        return max(0, self._hp)

    @hp.setter
    def hp(self, value):
        """修改生命值，限制范围0-200"""
        if not isinstance(value, (int, float)):
            raise ValueError("生命值必须是数字！")
        self._hp = max(0, min(value, 200))  # 限制在0-200之间

    # -------------------------- 4. 实例方法（操作属性） --------------------------
    def move(self, dx, dy):
        """移动玩家，修改私有坐标属性"""
        self.x += dx  # 用@property的setter修改_x（自动校验）
        # 直接修改双下划线私有属性（内部可访问）
        self.__y += dy

    def attack(self, damage):
        """受到攻击，减少生命值"""
        self.hp -= damage

    def __str__(self):
        """自定义打印格式"""
        return f"玩家[{self.name}] 位置：{self.position} 生命值：{self.hp} 总玩家数：{Player.player_count}"


# -------------------------- 测试用例：验证所有属性规则 --------------------------
if __name__ == "__main__":
    # 1. 创建实例，验证类属性和实例属性
    p1 = Player("张三", 10, 20)
    p2 = Player("李四", 30, 40)
    print("=== 1. 初始状态 ===")
    print(p1)  # 玩家[张三] 位置：(10, 20) 生命值：100 总玩家数：2
    print(p2)  # 玩家[李四] 位置：(30, 40) 生命值：100 总玩家数：2

    # 2. 访问/修改类属性
    print("\n=== 2. 类属性操作 ===")
    print("默认生命值（类访问）：", Player.DEFAULT_HP)  # 100
    print("p1的默认生命值（实例访问类属性）：", p1.DEFAULT_HP)  # 100

    # 实例修改类属性：会新增实例属性，遮蔽类属性
    p1.DEFAULT_HP = 150
    print("p1修改后DEFAULT_HP：", p1.DEFAULT_HP)  # 150（实例属性）
    print("Player.DEFAULT_HP：", Player.DEFAULT_HP)  # 100（类属性不变）
    del p1.DEFAULT_HP  # 删除实例属性，恢复访问类属性
    print("删除p1的DEFAULT_HP后：", p1.DEFAULT_HP)  # 100

    # 3. @property 访问和修改
    print("\n=== 3. @property 操作 ===")
    # 访问只读属性
    print("p1位置（只读）：", p1.position)  # (10, 20)
    # p1.position = (50, 50)  # 报错：无法修改只读属性

    # 修改x坐标（带校验）
    p1.x = 50  # 合法值
    print("p1修改x后位置：", p1.position)  # (50, 20)
    # p1.x = -10  # 报错：x坐标必须在0-1000之间

    # 修改生命值（带逻辑）
    p1.hp = 150
    print("p1生命值设为150：", p1.hp)  # 150
    p1.attack(80)
    print("p1受到80点伤害后生命值：", p1.hp)  # 70
    p1.hp = -50
    print("p1生命值设为-50（自动修正）：", p1.hp)  # 0

    # 4. 私有化属性访问规则
    print("\n=== 4. 私有化属性操作 ===")
    # 单下划线私有属性：外部可访问（不推荐）
    print("p1的_x（单下划线）：", p1._x)  # 50
    # 双下划线私有属性：名称改写，直接访问报错
    # print(p1.__y)  # 报错：'Player' object has no attribute '__y'
    # 双下划线属性的实际名称（_类名__属性名）
    print("p1的__y（实际名称）：", p1._Player__y)  # 20

    # 5. 实例方法修改私有属性
    print("\n=== 5. 实例方法操作 ===")
    p1.move(10, 15)
    print("p1移动后位置：", p1.position)  # (60, 35)
