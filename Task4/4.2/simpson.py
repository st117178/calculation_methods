from typing import Callable

class Simpson:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def integrate(self, func: Callable[[float], float]) -> float:
        return (self.b - self.a) / 6 * (func(self.a) + 4 * func((self.a + self.b) / 2) + func(self.b))

    def get_name(self) -> str:
        return "КФ Симпсона"
