from functions import Functions
from integrals import Integrals
from compound_left_rectangle import CompoundLeftRectangle
from compound_right_rectangle import CompoundRightRectangle
from compound_middle_rectangle import CompoundMiddleRectangle
from compound_trapezoid import CompoundTrapezoid
from compound_simpson import CompoundSimpson
from runge_romberg import RungeRomberg
from tabulate import tabulate

class Interface:
    def __init__(self):
        self.functions = None
        self.integrals = None
        self.quadratures = []

        self.a = 0.0
        self.b = 1.0
        self.m = 10
        self.h = 0.1
        self.selected_func_key = "f4"

        self._history = []
        self._results = {}

    @staticmethod
    def _input_float(prompt: str, default: float = None) -> float:
        while True:
            try:
                s = input(prompt).strip()
                if s == "" and default is not None:
                    return default
                return float(s)
            except ValueError:
                print("  Ошибка: введите число.")

    @staticmethod
    def _input_int(prompt: str, min_val: int = 1) -> int:
        while True:
            try:
                s = input(prompt).strip()
                val = int(s)
                if val < min_val:
                    print(f"  Число должно быть >= {min_val}")
                    continue
                return val
            except ValueError:
                print("  Ошибка: введите целое число.")

    @staticmethod
    def _input_choice(prompt: str, choices: list) -> str:
        while True:
            s = input(prompt).strip().lower()
            if s in choices:
                return s
            print(f"  Введите одно из: {', '.join(choices)}")

    def _dialog_greeting(self) -> None:
        print("\n" + "=" * 70)
        print("  Приближенное вычисление интеграла")
        print("  по составным квадратурным формулам")
        print("  Уточнение по Рунге-Ромбергу")
        print("=" * 70)

    def _dialog_parameters(self) -> None:
        print("\n" + "-" * 40)
        print("  Ввод параметров")
        print("-" * 40)

        self.a = self._input_float("  A = ")
        while True:
            self.b = self._input_float("  B = ")
            if self.b > self.a:
                break
            print(f"  B должно быть > A ({self.a})")

        self.m = self._input_int("  m (число промежутков) = ", min_val=1)
        self.h = (self.b - self.a) / self.m

        print(f"\n  Установлены параметры: A = {self.a}, B = {self.b}, m = {self.m}")
        print(f"  Шаг h = {self.h}")

    def _initialize_quadratures(self) -> None:
        self.quadratures = [
            CompoundLeftRectangle(self.a, self.b, self.m),
            CompoundRightRectangle(self.a, self.b, self.m),
            CompoundMiddleRectangle(self.a, self.b, self.m),
            CompoundTrapezoid(self.a, self.b, self.m),
            CompoundSimpson(self.a, self.b, self.m)
        ]

        self.integrals = Integrals(self.a, self.b)
        self.integrals.compute_all()

    def _dialog_select_function(self) -> None:
        print("\n" + "-" * 40)
        print("  Выбор функции для интегрирования")
        print("-" * 40)

        keys = self.functions.all_keys()
        print("  Доступные функции:")
        for key in keys:
            print(f"    {key}: {self.functions.get_name(key)}")

        self.selected_func_key = self._input_choice(
            f"  Ваш выбор ({'/'.join(keys)}): ",
            keys
        )
        print(f"  Выбрана функция: {self.functions.get_name(self.selected_func_key)}")

    def _dialog_compute(self) -> None:
        print("\n" + "-" * 40)
        print("  Результаты вычислений")
        print("-" * 40)

        _, func = self.functions.get_function(self.selected_func_key)
        exact = self.integrals.get_exact(self.selected_func_key)

        print(f"  Функция: {self.functions.get_name(self.selected_func_key)}")
        print(f"  Точное значение интеграла J = {exact}")

        self._results = {}
        table_data = []
        headers = ["Название СКФ", "J(h)", "|J - J(h)|", "|J - J(h)|/|J|"]

        for qf in self.quadratures:
            approx = qf.integrate(func)
            abs_err = abs(exact - approx)
            rel_err = abs_err / abs(exact) if abs(exact) > 1e-15 else abs_err

            self._results[qf.get_name()] = {
                'approx': approx,
                'abs_err': abs_err,
                'rel_err': rel_err,
                'ast': qf.get_ast()
            }

            table_data.append([
                qf.get_name(),
                approx,
                abs_err,
                rel_err
            ])

        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid",
                              floatfmt=(".17f", ".17f", ".17e", ".17e")))

    def _dialog_runge_romberg(self) -> None:
        print("\n" + "=" * 70)
        print("  Уточнение по Рунге-Ромбергу")
        print("=" * 70)

        l = self._input_int("  l (коэффициент увеличения числа разбиений) = ", min_val=2)

        new_m = self.m * l
        new_h = self.h / l

        print(f"\n  Новое число разбиений: m*l = {new_m}")
        print(f"  Новый шаг: h/l = {new_h}")

        _, func = self.functions.get_function(self.selected_func_key)
        exact = self.integrals.get_exact(self.selected_func_key)

        print("\n" + "-" * 70)
        print("  Вычисление с новым шагом h/l")
        print("-" * 70)

        new_quadratures = [
            CompoundLeftRectangle(self.a, self.b, new_m),
            CompoundRightRectangle(self.a, self.b, new_m),
            CompoundMiddleRectangle(self.a, self.b, new_m),
            CompoundTrapezoid(self.a, self.b, new_m),
            CompoundSimpson(self.a, self.b, new_m)
        ]

        table_data = []
        headers = [
            "Название СКФ",
            "J(h)",
            "|J-J(h)|",
            "Отн.погр.",
            "J(h/l)",
            "|J-J(h/l)|",
            "Отн.погр.",
            "J_уточн",
            "|J-J_уточн|",
            "Отн.погр."
        ]

        for i, qf in enumerate(self.quadratures):
            name = qf.get_name()
            j_h = self._results[name]['approx']
            abs_err_h = self._results[name]['abs_err']
            rel_err_h = self._results[name]['rel_err']
            ast = qf.get_ast()

            new_qf = new_quadratures[i]
            j_h_l = new_qf.integrate(func)
            abs_err_h_l = abs(exact - j_h_l)
            rel_err_h_l = abs_err_h_l / abs(exact) if abs(exact) > 1e-17 else abs_err_h_l

            j_refined = RungeRomberg.refine(j_h, j_h_l, l, ast)
            abs_err_refined = abs(exact - j_refined)
            rel_err_refined = abs_err_refined / abs(exact) if abs(exact) > 1e-17 else abs_err_refined

            table_data.append([
                name,
                j_h,
                abs_err_h,
                rel_err_h,
                j_h_l,
                abs_err_h_l,
                rel_err_h_l,
                j_refined,
                abs_err_refined,
                rel_err_refined
            ])

        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid",
                              floatfmt=(".17f", ".17f", ".7e", ".7e", ".17f", ".7e", ".7e", ".17f", ".7e", ".7e")))

    def _show_menu(self) -> str:
        print("\n" + "=" * 70)
        print("  [1] Выбрать другую функцию")
        print("  [2] Изменить параметры A, B, m")
        print("  [3] Повторить вычисление для текущей функции")
        print("  [4] Уточнение по Рунге-Ромбергу")
        if self._history:
            print("  [b] Вернуться на шаг назад")
        print("  [0] Выход")
        print("=" * 70)

        choices = ["0", "1", "2", "3", "4"]
        if self._history:
            choices.append("b")

        return self._input_choice("  Ваш выбор: ", choices)

    def _save_state(self) -> None:
        state = {
            'a': self.a,
            'b': self.b,
            'm': self.m,
            'h': self.h,
            'selected_func_key': self.selected_func_key
        }
        self._history.append(state)

    def _restore_state(self) -> None:
        if not self._history:
            return

        state = self._history.pop()
        self.a = state['a']
        self.b = state['b']
        self.m = state['m']
        self.h = state['h']
        self.selected_func_key = state['selected_func_key']

        self._initialize_quadratures()

        print("\n  Состояние восстановлено.")

    def run(self) -> None:
        self._dialog_greeting()

        self.functions = Functions()

        self._dialog_parameters()
        self._initialize_quadratures()
        self._dialog_select_function()
        self._dialog_compute()

        while True:
            choice = self._show_menu()

            if choice == "0":
                print("\n  Программа завершена.")
                break

            elif choice == "1":
                self._save_state()
                self._dialog_select_function()
                self._dialog_compute()

            elif choice == "2":
                self._save_state()
                self._dialog_parameters()
                self._initialize_quadratures()
                self._dialog_select_function()
                self._dialog_compute()

            elif choice == "3":
                self._dialog_compute()

            elif choice == "4":
                self._dialog_runge_romberg()

            elif choice == "b":
                self._restore_state()
                self._dialog_compute()

            print()
