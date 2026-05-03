from typing import Callable

class Functions:
    def __init__(self):
        self._funcs = {}

        self._register("f0", "f0(x) = 1", lambda x: 1.0)
        self._register("f1", "f1(x) = x", lambda x: x)
        self._register("f2", "f2(x) = x^2", lambda x: x**2)
        self._register("f3", "f3(x) = x^3", lambda x: x**3)

        self._funcs["f4"] = None

        import math
        self._register("f5", "f5(x) = sin(x)", lambda x: math.sin(x))

    def _register(self, key: str, name: str, func: Callable[[float], float]) -> None:
        self._funcs[key] = (name, func)

    def register_polynomial(self, N: int) -> None:
        degree = N - 1
        name = f"f4(x) = x^{degree} + 1"
        func = lambda x, d=degree: x**d + 1.0

        self._funcs["f4"] = (name, func)

    def get_function(self, key: str) -> tuple:
        if key not in self._funcs:
            raise KeyError(f"Функция с ключом '{key}' не существует.")
        if self._funcs[key] is None:
            raise ValueError(f"Функция '{key}' ещё не инициализирована (возможно, не вызван register_polynomial).")
        return self._funcs[key]

    def get_name(self, key: str) -> str:
        return self.get_function(key)[0]

    def evaluate(self, key: str, x: float) -> float:
        return self.get_function(key)[1](x)

    def all_keys(self) -> list:
        return [k for k, v in self._funcs.items() if v is not None]