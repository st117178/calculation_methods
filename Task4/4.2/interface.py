from functions import Functions
from integrals import Integrals
from left_rectangle import LeftRectangle
from right_rectangle import RightRectangle
from middle_rectangle import MiddleRectangle
from trapezoid import Trapezoid
from simpson import Simpson

class Interface:
    def __init__(self):
        self.functions = None
        self.integrals = None
        self.quadratures = []

        self.a = 0.0
        self.b = 1.0
        self.selected_func_key = "f4"

        self._history = []

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
    def _input_choice(prompt: str, choices: list) -> str:
        while True:
            s = input(prompt).strip().lower()
            if s in choices:
                return s
            print(f"  Введите одно из: {', '.join(choices)}")

    def _dialog_greeting(self) -> None:
        print("\n" + "=" * 60)
        print("  Приближенное вычисление интеграла")
        print("  по простейшим квадратурным формулам")
        print("=" * 60)

    def _dialog_interval(self) -> None:
        print("\n" + "-" * 40)
        print("  Ввод границ интегрирования [a, b]")
        print("-" * 40)

        self.a = self._input_float("  a = ")
        while True:
            self.b = self._input_float("  b = ")
            if self.b > self.a:
                break
            print(f"  b должно быть > a ({self.a})")

        print(f"\n  Установлены границы: a = {self.a}, b = {self.b}")

    def _initialize_quadratures(self) -> None:
        self.quadratures = [
            LeftRectangle(self.a, self.b),
            RightRectangle(self.a, self.b),
            MiddleRectangle(self.a, self.b),
            Trapezoid(self.a, self.b),
            Simpson(self.a, self.b)
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
        print(f"  Точное значение интеграла: {exact:.17f}")
        print("\n" + "-" * 60)

        for qf in self.quadratures:
            approx = qf.integrate(func)
            abs_err = abs(exact - approx)

            print(f"\n  {qf.get_name()}")
            print(f"    Приближенное значение: {approx:.17f}")
            print(f"    Абсолютная погрешность: {abs_err:.17e}")

        print("-" * 60)

    def _show_menu(self) -> str:
        print("\n" + "=" * 60)
        print("  [1] Выбрать другую функцию")
        print("  [2] Изменить границы [a, b]")
        print("  [3] Повторить вычисление для текущей функции")
        if self._history:
            print("  [b] Вернуться на шаг назад")
        print("  [0] Выход")
        print("=" * 60)

        choices = ["0", "1", "2", "3"]
        if self._history:
            choices.append("b")

        return self._input_choice("  Ваш выбор: ", choices)

    def _save_state(self) -> None:
        state = {
            'a': self.a,
            'b': self.b,
            'selected_func_key': self.selected_func_key
        }
        self._history.append(state)

    def _restore_state(self) -> None:
        if not self._history:
            return

        state = self._history.pop()
        self.a = state['a']
        self.b = state['b']
        self.selected_func_key = state['selected_func_key']

        self._initialize_quadratures()

        print("\n  Состояние восстановлено.")

    def run(self) -> None:
        self._dialog_greeting()

        self.functions = Functions()

        self._dialog_interval()
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
                self._dialog_interval()
                self._initialize_quadratures()
                self._dialog_select_function()
                self._dialog_compute()

            elif choice == "3":
                self._dialog_compute()

            elif choice == "b":
                self._restore_state()
                self._dialog_compute()

            print()
