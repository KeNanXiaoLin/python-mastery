class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")


if __name__ == "__main__":
    a = 100
    b = 100
    print(f"a: {id(a)}, b: {id(b)}, a is b: {a is b}")  # True
    l1 = [1, 2, 3]
    l2 = [1, 2, 3]
    print(f"l1: {id(l1)}, l2: {id(l2)}, l1 is l2: {l1 is l2}")  # False
    p1 = Person("Alice", 30)
    Person.speak(p1)  # Hello, my name is Alice and I am 30 years old.
    p1.name  # get an attr
    p1.age = 18  # set an attr
    del p1.name  # delete an attr
    getattr(p1, "age")  # get an attr
    setattr(p1, "age", 20)  # set an attr
    delattr(p1, "age")  # delete an attr
    hasattr(p1, "age")  # check if an attr exists
