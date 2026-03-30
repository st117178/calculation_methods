from typing import Callable, Literal, List, Tuple, Dict
import random
from tabulate import tabulate

class DataProvider:
    def __init__(
            self,
            *,
            func: Callable[[float], float],
            count_points: int,
            type_filling: Literal["random", "equally"],
            interval: Tuple[int]
        ):
        self.func = func
        self.m = count_points
        self.type_filling = type_filling
        self.interval = interval

        self.table = self.generate_table_equal() if self.type_filling == "equally" else self.generate_tabel_random()

    
    def generate_table_equal(self) -> Dict[str, List[float]]:
        func_table = []
        z_table = []

        h = (self.interval[1] - self.interval[0])/self.m
        for k in range(self.m + 1):
            zk = self.interval[0] + k*h
            z_table.append(zk)
            func_table.append(self.func(zk))

        dict_table = {
            "z_k": z_table,
            "f_zk": func_table
        }
        return dict_table


    def generate_tabel_random(self) -> Dict[str, List[float]]:
        func_table = []
        z_table = []

        for _ in range(self.m - 1):
            zk = random.uniform(self.interval[0], self.interval[1])
            z_table.append(zk)
            func_table.append(self.func(zk))

        z_table.append(self.interval[0])
        z_table.append(self.interval[1])

        func_table.append(self.func(self.interval[0]))
        func_table.append(self.func(self.interval[1]))

        sorted_table = sorted(zip(z_table, func_table))
        z_table, func_table = zip(*sorted_table)

        dict_table = {
            "z_k": list(z_table),
            "f_zk": list(func_table)
        }
        return dict_table
    

    def print_table(self):
        print(tabulate(
            self.table,
            headers="keys",
            tablefmt="grid",
            floatfmt=(".2f", ".2f"),
            missingval="—"
        ))