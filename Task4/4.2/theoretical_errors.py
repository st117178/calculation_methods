import math
from typing import Callable

class TheoreticalErrors:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def _estimate_max_derivative(self, func_key: str, order: int) -> float:
        num_samples = 1000
        h = (self.b - self.a) / num_samples
        max_val = 0.0

        if func_key == "f0":
            return 0.0 if order > 0 else 1.0
        elif func_key == "f1":
            if order == 0:
                return max(abs(self.a), abs(self.b))
            elif order == 1:
                return 1.0
            else:
                return 0.0
        elif func_key == "f2":
            if order == 0:
                return max(abs(self.a**2), abs(self.b**2))
            elif order == 1:
                return max(abs(2*self.a), abs(2*self.b))
            elif order == 2:
                return 2.0
            else:
                return 0.0
        elif func_key == "f3":
            if order == 0:
                return max(abs(self.a**3), abs(self.b**3))
            elif order == 1:
                return max(abs(3*self.a**2), abs(3*self.b**2))
            elif order == 2:
                return max(abs(6*self.a), abs(6*self.b))
            elif order == 3:
                return 6.0
            else:
                return 0.0
        elif func_key == "f4":
            for i in range(num_samples + 1):
                x = self.a + i * h
                if order == 1:
                    val = abs(math.cos(x))
                elif order == 2:
                    val = abs(-math.sin(x))
                elif order == 4:
                    val = abs(math.sin(x))
                else:
                    val = 0.0
                max_val = max(max_val, val)
            return max_val

        return 0.0

    def left_rectangle(self, func_key: str) -> float:
        max_f_prime = self._estimate_max_derivative(func_key, 1)
        return 0.5 * (self.b - self.a)**2 * max_f_prime

    def right_rectangle(self, func_key: str) -> float:
        max_f_prime = self._estimate_max_derivative(func_key, 1)
        return 0.5 * (self.b - self.a)**2 * max_f_prime

    def middle_rectangle(self, func_key: str) -> float:
        max_f_double_prime = self._estimate_max_derivative(func_key, 2)
        return (1.0/24.0) * (self.b - self.a)**3 * max_f_double_prime

    def trapezoid(self, func_key: str) -> float:
        max_f_double_prime = self._estimate_max_derivative(func_key, 2)
        return (1.0/12.0) * (self.b - self.a)**3 * max_f_double_prime

    def simpson(self, func_key: str) -> float:
        max_f_fourth = self._estimate_max_derivative(func_key, 4)
        return (1.0/2880.0) * (self.b - self.a)**5 * max_f_fourth
