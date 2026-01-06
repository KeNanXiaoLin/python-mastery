import sys


if __name__ == "__main__":
    a = 100
    print(sys.getsizeof(a))  # 28
    b = 100.0
    print(sys.getsizeof(b))  # 24
    c = "H"
    print(sys.getsizeof(c))  # 62
