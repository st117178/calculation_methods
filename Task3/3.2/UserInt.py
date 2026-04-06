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
                idx = int(choice) - 1
                if 0 <= idx < len(self.functions):
                    self.process_function(self.functions[idx])
                else:
                    print("\nОшибка: выберите корректный номер из списка.")
            except ValueError:
                print("\nОшибка: введите число.")

    def process_function(self, func):
        while True:
            print(f"\nРабота с функцией: {func.name}")
            print("Введите 'b' для возврата в главное меню.")
            
            user_input = input("Введите x0, h, m (через пробел): ")
            if user_input.lower() == 'b': return
            
            try:
                parts = user_input.split()
                if len(parts) != 3: continue
                x0, h, m = float(parts[0]), float(parts[1]), int(parts[2])
                
                if m < 2:
                    print("Ошибка: m должно быть >= 2 для расчета хотя бы O(h^2).")
                    continue
            except ValueError:
                print("Ошибка ввода. Ожидается: [x0] [h] [m]"); continue

            dm = DataManager(func)
            dm.generate_table(x0, h, m)
            
            nm = NumericalMethods(dm.y_values, h)
            df_h2 = nm.get_first_derivative_oh2()
            df_h4 = nm.get_first_derivative_oh4()
            ddf_h2 = nm.get_second_derivative_oh2()
            exact_df, exact_ddf = dm.get_exact_derivatives()

            main_table_data = []
            for i in range(len(dm.x_nodes)):
                if df_h4[i] is not None:
                    h4_val = f"{df_h4[i]:.10f}"
                    h4_err = f"{abs(exact_df[i] - df_h4[i]):.2e}"
                else:
                    h4_val, h4_err = "---", "---"

                if ddf_h2[i] is not None:
                    d2_val = f"{ddf_h2[i]:.10f}"
                    d2_err = f"{abs(exact_ddf[i] - ddf_h2[i]):.2e}"
                else:
                    d2_val, d2_err = "---", "---"

                main_table_data.append([
                    f"{dm.x_nodes[i]:.4f}",
                    f"{dm.y_values[i]:.10f}",
                    f"{exact_df[i]:.10f}",
                    f"{df_h2[i]:.10f}",
                    f"{abs(exact_df[i] - df_h2[i]):.2e}",
                    h4_val, h4_err,
                    f"{exact_ddf[i]:.10f}",
                    d2_val, d2_err
                ])

            headers = ["x_k", "y_k", "f'_T", "f' O(h2)", "погр. O(h2)", 
                       "f' O(h4)", "погр. O(h4)", "f''_T", "f'' O(h2)", "погр. O(h2)"]
            
            print(f"\nТаблица 1: Результаты (m={m}, h={h})")
            print(tabulate(main_table_data, headers=headers, tablefmt="fancy_grid", 
                               floatfmt=(".6f", ".10f", ".10f", ".10f", ".10e",
                                          ".10f", ".10e", ".10f", ".10f", ".10e")))

            if input("\nВыполнить подбор оптимального шага в x0? (y/n): ").lower() == 'y':
                opt_data = nm.find_optimal_step(func, x0)
                opt_headers = ["Шаг h", "f'(x0)_Е", "f'(x0) O(h2)", "погр."]
                print(tabulate(opt_data, headers=opt_headers, tablefmt="fancy_grid", 
                               floatfmt=(".8f", ".10f", ".10f", ".2e")))
                h = opt_data[-2][0]
                print(f"\nОптимальный шаг {h = }")

            if input("\nИзменить параметры для этой функции? (y/n): ").lower() != 'y':
                break