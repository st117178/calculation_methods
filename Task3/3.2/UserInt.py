from DataManager import DataManager
from NumMethods import NumericalMethods

from tabulate import tabulate

class UserInterface:
    def __init__(self, functions):
        self.functions = functions

    def run(self):
        while True:
            print("Вычисление производных для таблично заданной функции.")
            for i, func in enumerate(self.functions, 1):
                print(f"{i}. {func.name}")
            print("0. Выход")
            
            choice = input("\nВыберите номер функции: ")
            if choice == '0': break
            
            try:
                selected_func = self.functions[int(choice)-1]
                self.process_function(selected_func)
            except (ValueError, IndexError):
                print("Ошибка: выберите число из списка.")

    def process_function(self, func):
        while True:
            print(f"\n--- Работа с функцией: {func.name} ---")
            print("Введите 'b' для возврата в главное меню.")
            
            user_input = input("Введите x0, h, m (через пробел): ")
            if user_input.lower() == 'b': return
            try:
                x0, h, m = map(float, user_input.split())
                m = int(m)
                if m < 4:
                    print("Ошибка: m должно быть >= 4 для корректного расчета O(h^4).")
                    continue
            except ValueError:
                print("Ошибка ввода. Ожидается: [число] [число] [целое число]"); continue

            dm = DataManager(func)
            dm.generate_table(x0, h, m)
            
            nm = NumericalMethods(dm.y_values, h)
            df_h2 = nm.get_first_derivative_oh2()
            df_h4 = nm.get_first_derivative_oh4()
            ddf_h2 = nm.get_second_derivative_oh2()
            exact_df, exact_ddf = dm.get_exact_derivatives()

            main_table_data = []
            for i in range(len(dm.x_nodes)):
                main_table_data.append([
                    dm.x_nodes[i],
                    dm.y_values[i],
                    exact_df[i],
                    df_h2[i],
                    abs(exact_df[i] - df_h2[i]),
                    df_h4[i],
                    abs(exact_df[i] - df_h4[i]),
                    exact_ddf[i],
                    ddf_h2[i],
                    abs(exact_ddf[i] - ddf_h2[i])
                ])

            headers = ["x", "y", "f' exact", "f' O(h2)", "Error(O(h2))", "f' O(h4)", "Error(O(h4))", "f'' exact", "f'' O(h2)", "Error(O(h2))"]
            print("\nТаблица 1: Результаты численного дифференцирования")
            print(tabulate(main_table_data, headers=headers, tablefmt="grid", floatfmt=".10f"))

            if input("\nВыполнить подбор оптимального шага в x0? (y/n): ").lower() == 'y':
                opt_data = nm.find_optimal_step(func, x0)
                opt_headers = ["Шаг h", "Точная f'(x0)", "Приближ. f'(x0)", "Факт. погрешность"]
                print("\nТаблица 2: Поиск оптимального шага")
                print(tabulate(opt_data, headers=opt_headers, tablefmt="fancy_grid", floatfmt=(".8f", ".6f", ".6f", ".2e")))

            if input("\nИзменить параметры x0, h, m для этой функции? (y/n): ").lower() != 'y':
                break