import scipy.integrate as integrate
from typing import Callable

class Moments:
    def __init__(self, a: float, b: float, weight_func: Callable[[float], float], breakpoints: list = None):
        self.a = a
        self.b = b
        self.weight = weight_func
        self.breakpoints = breakpoints if breakpoints else []
        
        self._cache = {}
    
    def compute(self, m: int) -> float:
        if m in self._cache:
            return self._cache[m]
        
        def integrand(x: float) -> float:
            return self.weight(x) * (x ** m)
        
        points = [p for p in self.breakpoints if self.a < p < self.b]
        if not points:
            points = None
        
        result, error = integrate.quad(
            integrand, 
            self.a, self.b, 
            points=points,
            limit=200,
            epsabs=1e-14,
            epsrel=1e-14
        )
                
        self._cache[m] = result
        return result
    
    def compute_range(self, max_m: int) -> list:
        return [self.compute(m) for m in range(max_m + 1)]
    
    def clear_cache(self) -> None:
        self._cache.clear()