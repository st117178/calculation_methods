from typing import List, Tuple, Dict, TypedDict
from tabulate import tabulate

class FunctionTable(TypedDict):
    z_k: List[float]
    f_zk: List[float]


class Interpolation:
    def __init__(
            self,
            *,
            table: FunctionTable,
            n: int
        ):
        self.table = table
        self.n = n


    def get_f_zk(self, *, zk: float):
        lookup = dict(zip(self.table['z_k'], self.table['f_zk']))
        return lookup.get(zk)
    

    def sorted_x(self, *, x: float) -> List[float]:
        x_table = self.table['z_k']
        sorted_nodes = sorted(x_table, key=lambda xk: abs(x - xk))
    
        return sorted(sorted_nodes[:self.n + 1])


    def polynom_lagrange(self, *, x: float):
        xk_table = self.sorted_x(x=x)
        Pn_x = 0
        for i in range(self.n + 1):
            Li_x = 1
            for j in range(self.n + 1):
                if i == j:
                    continue
                Li_x *= (x - xk_table[j])/(xk_table[i] - xk_table[j])
            Pn_x += self.get_f_zk(zk=xk_table[i]) * Li_x

        return Pn_x
    

    def polynom_newton(self, *, x: float):
        xk_table = self.sorted_x(x=x)
        yk_table = [self.get_f_zk(zk=zk) for zk in xk_table]
        
        num_points = self.n + 1
        
        res_diffs = [yk_table]
        
        for i in range(1, num_points):
            current_level = []
            for j in range(num_points - i):
                numerator = res_diffs[i-1][j+1] - res_diffs[i-1][j]
                denominator = xk_table[j + i] - xk_table[j]
                current_level.append(numerator / denominator)
            res_diffs.append(current_level)

        coefficients = [level[0] for level in res_diffs]
        
        pn_x = coefficients[0]
        product_term = 1
        
        for i in range(1, num_points):
            product_term *= (x - xk_table[i-1])
            pn_x += coefficients[i] * product_term
        self.print_diff_table(xk_table=xk_table, res_diffs=res_diffs)
        return pn_x
    

    def print_diff_table(self, *, xk_table: list, res_diffs: list):
        headers = ["z_k", "f(z_k)"]
        for i in range(1, len(res_diffs)):
            headers.append(f"{i}-я разность")

        rows = []
        num_rows = len(xk_table)
        
        for i in range(num_rows):
            row = [xk_table[i]]
            
            for col in range(len(res_diffs)):
                if i < len(res_diffs[col]):
                    row.append(res_diffs[col][i])
                else:
                    row.append("")
            
            rows.append(row)

        print("\nТаблица разделенных разностей:")
        print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".6f"))

    
    def error(self, *, f_x: float, Pn_x: float):
        return abs(Pn_x - f_x)