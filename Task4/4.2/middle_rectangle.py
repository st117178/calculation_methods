from typing import Callable

class MiddleRectangle:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def integrate(self, func: Callable[[float], float]) -> float:
        return (self.b - self.a) * func((self.a + self.b) / 2)

    def get_name(self) -> str:
        return "КФ среднего прямоугольника"
