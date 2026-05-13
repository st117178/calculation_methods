from typing import Callable

class LeftRectangle:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def integrate(self, func: Callable[[float], float]) -> float:
        return (self.b - self.a) * func(self.a)

    def get_name(self) -> str:
        return "КФ левого прямоугольника"
