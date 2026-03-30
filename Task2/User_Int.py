from typing import Callable

from Interpolation import Interpolation, tabulate
from DataProvider import DataProvider


class UserInterface:
    def __init__(self, func: Callable[[float], float]):
        self.func = func
        self.provider = None

    def _input_float(self, prompt: str) -> float:
        while True:
            try:
                return float(input(prompt).replace(',', '.'))
            except ValueError:
                print("Ошибка: введите числовое значение.")

    def _input_int(self, prompt: str, min_val: int = None, max_val: int = None) -> int:
        while True:
            try:
                val = int(input(prompt))
                if min_val is not None and val < min_val:
                    print(f"Ошибка: число должно быть не меньше {min_val}.")
                    continue
                if max_val is not None and val > max_val:
                    print(f"Ошибка: число должно быть не больше {max_val}.")
                    continue
                return val
            except ValueError:
                print("Ошибка: введите целое число.")

    def setup_table(self):
        print("Задача алгебраического интерполирования. Вариант 7. f(x)=exp(–x) – x^2/2, a=0, b=5, m+1=26, n=10")


        m_plus_1 = self._input_int("Введите число значений в таблице (m+1): ", min_val=2)
        
        while True:
            a = self._input_float("Введите левую границу отрезка (a): ")
            b = self._input_float("Введите правую границу отрезка (b): ")
            if a < b:
                break
            print("Ошибка: левая граница должна быть меньше правой.")

        while True:
            fill_type = input(f"Тип заполнения таблицы (1 - равномерно(h = {(b-a)/(m_plus_1-1)}), 2 - случайно): ").strip()
            if fill_type == "1":
                t_type = "equally"
                break
            elif fill_type == "2":
                t_type = "random"
                break
            print("Ошибка: выберите 1 или 2.")

        self.provider = DataProvider(
            func=self.func,
            count_points=m_plus_1 - 1,
            type_filling=t_type,
            interval=(a, b)
        )
        
        print("\nИсходная таблица значений функции:")
        self.provider.print_table()

    def run(self):
        self.setup_table()
        m = self.provider.m

        while True:
            x = self._input_float("Введите точку интерполирования x (или 'exit' для выхода): ")
            
            while True:
                n = self._input_int(f"Введите степень многочлена n (n <= {m}): ", min_val=0)
                if n <= m:
                    break
                print(f"Введено недопустимое значение n <= {m}.")

            interp = Interpolation(table=self.provider.table, n=n)
            
            chosen_nodes = interp.sorted_x(x=x)
            print(f"\nВыбрано {n+1} ближайших узлов для x = {x}:")
            nodes_to_display = []
            for node in chosen_nodes:
                nodes_to_display.append([node, self.func(node)])
            
            print(tabulate(
                nodes_to_display, 
                headers=["z_k", "f(z_k)"], 
                tablefmt="grid", 
                floatfmt=".6f"
            ))
            original_print_diff = interp.print_diff_table
            if n > 10:
                interp.print_diff_table = lambda **kwargs: None

            f_actual = self.func(x)
            
            p_lagrange = interp.polynom_lagrange(x=x)
            e_lagrange = interp.error(f_x=f_actual, Pn_x=p_lagrange)
            
            p_newton = interp.polynom_newton(x=x)
            e_newton = interp.error(f_x=f_actual, Pn_x=p_newton)

            print(f"\nРезультаты вычислений для x = {x}:")
            print(f"Значение функции f(x): {f_actual:.12f}")
            print(f"{'Метод':<15} | {'Значение Pn(x)':<18} | {'Абс. погрешность':<18}")
            print(f"{'Лагранж':<15} | {p_lagrange:<18.12f} | {e_lagrange:<18.12e}")
            print(f"{'Ньютон':<15} | {p_newton:<18.12f} | {e_newton:<18.12e}")

            choice = input("\nПродолжить работу с текущей таблицей? (y/n): ").lower().strip()
            if choice != 'y':
                choice_main = input("Начать новую таблицу или выйти? (1 - новую, 0 - выход): ").strip()
                if choice_main == "1":
                    self.setup_table()
                    m = self.provider.m
                else:
                    break