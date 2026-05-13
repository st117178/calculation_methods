from typing import Callable

class Trapezoid:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def integrate(self, func: Callable[[float], float]) -> float:
        return (self.b - self.a) / 2 * (func(self.a) + func(self.b))

    def get_name(self) -> str:
        return "КФ трапеции"
