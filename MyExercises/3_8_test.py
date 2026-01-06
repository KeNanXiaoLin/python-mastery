class Parent:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def spam(self):
        print("Parent.spam")


class A(Parent):
    def __init__(self, name, age):
        super().__init__(name, age)

    def spam(self):
        print("A.spam")
        super().spam()


class B(Parent):
    def spam(self):
        print("B.spam")
        super().spam()


class Child(A, B):
    pass


if __name__ == "__main__":
    child = Child("GOOG", 20)
    child.spam()  # 先打印A.spam，再打印B.spam，最后打印Parent.spam
    print(Parent.__dict__)  # 查看方法解析顺序
