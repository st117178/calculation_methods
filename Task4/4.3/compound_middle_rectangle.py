from typing import Callable

class CompoundMiddleRectangle:
    def __init__(self, a: float, b: float, m: int):
        self.a = a
        self.b = b
        self.m = m
        self.h = (b - a) / m

    def integrate(self, func: Callable[[float], float]) -> float:
        result = 0.0
        for j in range(self.m):
            result += func(self.a + j * self.h + self.h / 2)
        return self.h * result

    def get_name(self) -> str:
        return "СКФ средних прямоугольников"

    def get_ast(self) -> int:
        return 1
