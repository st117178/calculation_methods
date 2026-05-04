import numpy as np
from typing import Callable

class Quadrature:
    def __init__(self):
        self.N = 0
        self.nodes = []    
        self.coeffs = []   
        self._built = False

        self.a = 0.0
        self.b = 0.0
    
    def build(self, N: int, user_nodes: list, a: float, b: float, 
              moments_obj) -> None:
        if N < 1:
            raise ValueError("N должно быть >= 1")
        if len(user_nodes) != N:
            raise ValueError(f"Ожидалось {N} узлов, получено {len(user_nodes)}")

        if len(set(user_nodes)) != N:
            raise ValueError("Узлы должны быть попарно различны")
        
        self.N = N
        self.nodes = list(user_nodes)
        self.a = a
        self.b = b
        
        mu = moments_obj.compute_range(N - 1)
        
        V = np.zeros((N, N))
        for m in range(N):
            for k in range(N):
                V[m, k] = self.nodes[k] ** m

        mu_vec = np.array(mu)
        self.coeffs = np.linalg.solve(V, mu_vec).tolist()
        
        self._built = True
    
    def is_built(self) -> bool:
        return self._built
    
    def get_nodes(self) -> list:
        return self.nodes.copy()
    
    def get_coeffs(self) -> list:
        return self.coeffs.copy()
    
    def integrate(self, func: Callable[[float], float]) -> float:
        if not self._built:
            raise RuntimeError("КФ ещё не построена. Вызовите build().")
        
        result = 0.0
        for k in range(self.N):
            result += self.coeffs[k] * func(self.nodes[k])
        return result
    
    def check_accuracy(self, poly_func: Callable[[float], float], 
                       exact_integral: float) -> float:
        if not self._built:
            raise RuntimeError("КФ ещё не построена.")
        
        approx = self.integrate(poly_func)
        diff = abs(exact_integral - approx)
        return diff
    
    def print_info(self, functions_obj) -> str:
        if not self._built:
            return "КФ не построена."
        
        lines = []
        lines.append(f"Количество узлов N = {self.N}")
        lines.append("-" * 45)
        lines.append(f"{'k':>4} {'Узел x_k':>15} {'Коэфф. A_k':>15}")
        lines.append("-" * 45)
        
        sum_A = 0.0
        sum_abs_A = 0.0
        
        for k in range(self.N):
            lines.append(f"{k+1:>4} {self.nodes[k]:>15.8f} {self.coeffs[k]:>15.10f}")
            sum_A += self.coeffs[k]
            sum_abs_A += abs(self.coeffs[k])
        
        lines.append("-" * 45)
        lines.append(f"{'Сумма A_k:':>20} {sum_A:>15.10f}")
        lines.append(f"{'Сумма |A_k|:':>20} {sum_abs_A:>15.10f}")
        lines.append("-" * 45)
        
        return "\n".join(lines)