from typing import Callable
import math

class Functions:
    def __init__(self):
        self._funcs = {}

        self._register("f0", "f0(x) = 1", lambda x: 1.0)
        self._register("f1", "f1(x) = x", lambda x: x)
        self._register("f2", "f2(x) = x^2", lambda x: x**2)
        self._register("f3", "f3(x) = x^3", lambda x: x**3)
        self._register("f4", "f4(x) = sin(x)", lambda x: math.sin(x))

    def _register(self, key: str, name: str, func: Callable[[float], float]) -> None:
        self._funcs[key] = (name, func)

    def get_function(self, key: str) -> tuple:
        if key not in self._funcs:
            raise KeyError(f"Функция с ключом '{key}' не существует.")
        return self._funcs[key]

    def get_name(self, key: str) -> str:
        return self.get_function(key)[0]

    def evaluate(self, key: str, x: float) -> float:
        return self.get_function(key)[1](x)

    def all_keys(self) -> list:
        return list(self._funcs.keys())
