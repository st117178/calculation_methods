import scipy.integrate as integrate
from typing import Callable

class Integrals:
    def __init__(self, a: float, b: float, functions_obj, weight_func: Callable[[float], float]):
        self.a = a
        self.b = b
        self.functions = functions_obj
        self.weight = weight_func

        self._exact_values = {}

    def compute_all(self) -> None:
        for key in self.functions.all_keys():
            self._exact_values[key] = self._compute_for_key(key)

    def _compute_for_key(self, key: str) -> float:
        name, func = self.functions.get_function(key)

        def integrand(x: float) -> float:
            return self.weight(x) * func(x)

        break_point = 0.5
        if self.a < break_point < self.b:
            points = [break_point]
        else:
            points = None

        result, error = integrate.quad(integrand, self.a, self.b, 
                                       points=points,
                                       limit=200,   
                                       epsabs=1e-12,
                                       epsrel=1e-12)

        if error > 1e-10:
            print(f"  [Внимание] Интегрирование для {name}: оценка ошибки = {error:.2e}")
        
        return result

    def get_exact(self, key: str) -> float:
        if key not in self._exact_values:
            raise KeyError(f"Интеграл для '{key}' не был вычислен. Сначала вызовите compute_all().")
        return self._exact_values[key]

    def get_all_values(self) -> dict:
        return self._exact_values.copy()