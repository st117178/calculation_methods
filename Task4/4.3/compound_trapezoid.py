from typing import Callable

class CompoundTrapezoid:
    def __init__(self, a: float, b: float, m: int):
        self.a = a
        self.b = b
        self.m = m
        self.h = (b - a) / m

    def integrate(self, func: Callable[[float], float]) -> float:
        f0 = func(self.a)
        fm = func(self.b)

        w = 0.0
        for j in range(1, self.m):
            w += func(self.a + j * self.h)

        return self.h / 2 * (f0 + fm + 2 * w)

    def get_name(self) -> str:
        return "СКФ трапеций"

    def get_ast(self) -> int:
        return 1
