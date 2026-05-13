from typing import Callable

class CompoundSimpson:
    def __init__(self, a: float, b: float, m: int):
        self.a = a
        self.b = b
        self.m = m
        self.h = (b - a) / m

    def integrate(self, func: Callable[[float], float]) -> float:
        f0 = func(self.a)
        fm = func(self.b)
        z = f0 + fm

        w = 0.0
        for j in range(1, self.m):
            w += func(self.a + j * self.h)

        q = 0.0
        for j in range(self.m):
            q += func(self.a + j * self.h + self.h / 2)

        return self.h / 6 * (z + 2 * w + 4 * q)

    def get_name(self) -> str:
        return "СКФ Симпсона"

    def get_ast(self) -> int:
        return 3
