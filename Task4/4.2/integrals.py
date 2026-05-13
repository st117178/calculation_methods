import math

class Integrals:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b
        self._exact_values = {}

    def compute_all(self) -> None:
        self._exact_values["f0"] = self._compute_f0()
        self._exact_values["f1"] = self._compute_f1()
        self._exact_values["f2"] = self._compute_f2()
        self._exact_values["f3"] = self._compute_f3()
        self._exact_values["f4"] = self._compute_f4()

    def _compute_f0(self) -> float:
        return self.b - self.a

    def _compute_f1(self) -> float:
        return (self.b**2 - self.a**2) / 2

    def _compute_f2(self) -> float:
        return (self.b**3 - self.a**3) / 3

    def _compute_f3(self) -> float:
        return (self.b**4 - self.a**4) / 4

    def _compute_f4(self) -> float:
        return -math.cos(self.b) + math.cos(self.a)

    def get_exact(self, key: str) -> float:
        if key not in self._exact_values:
            raise KeyError(f"Интеграл для '{key}' не был вычислен.")
        return self._exact_values[key]

    def get_all_values(self) -> dict:
        return self._exact_values.copy()
