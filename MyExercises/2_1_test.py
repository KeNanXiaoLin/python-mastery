from dataclasses import dataclass
from typing import NamedTuple
from collections import namedtuple


@dataclass
class Stock:
    name: str
    shares: int
    price: float


class Stock2(NamedTuple):
    name: str
    shares: int
    price: float


if __name__ == "__main__":
    s = Stock("GOOG", 100, 490.1)
    print(s.name, s.shares * s.price)
    s2 = Stock2("GOOG", 100, 490.1)
    print(s2.name, s2.shares * s2.price)
    Stock3 = namedtuple("Stock3", ["name", "shares", "price"])
    s3 = Stock3("GOOG", 100, 490.1)
    print(s3[0])  # GOOG
    print(s3.name)  # GOOG
    print(isinstance(s3, tuple))  # True
    s3.name = "APPL"  # This will raise an AttributeError
