from typing import Callable

class CompoundRightRectangle:
    def __init__(self, a: float, b: float, m: int):
        self.a = a
        self.b = b
        self.m = m
        self.h = (b - a) / m

    def integrate(self, func: Callable[[float], float]) -> float:
        result = 0.0
        for j in range(1, self.m + 1):
            result += func(self.a + j * self.h)
        return self.h * result

    def get_name(self) -> str:
        return "СКФ правых прямоугольников"

    def get_ast(self) -> int:
        return 0
