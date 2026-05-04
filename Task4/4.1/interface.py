from functions import Functions
from weight import Weight
from integrals import Integrals
from moments import Moments
from quadrature import Quadrature

class Interface:
    def __init__(self):
        self.weight = None
        self.functions = None
        self.integrals = None
        self.moments = None
        self.quadrature = None

        self.a = 0.0
        self.b = 1.0
        self.N = 0
        self.selected_func_key = "f5"

        self._first_run = True
    
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
        self.weight = Weight()
        print("\n" + "=" * 55)
        print("  Построение ИКФ и приближённое вычисление интеграла")
        print("=" * 55)
        print(f"  Вариант {self.weight.get_variant()}")
        print(f"  Весовая функция: {self.weight.get_description()}")
        print(f"  Тестовая функция: f(x) = sin(x)")
        print(f"  Промежуток [a, b]: [0, 1]")
        print("=" * 55)
    
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
    
    def _dialog_nodes(self) -> None:
        print("\n" + "-" * 40)
        print("  Ввод параметров КФ")
        print("-" * 40)
        
        self.N = self._input_int("  Количество узлов N = ", min_val=1)
        
        print("\n  Способ задания узлов:")
        print("    1.Ввести вручную")
        print("    2.Сгенерировать равноотстоящие на [{}, {}]".format(self.a, self.b))
        
        choice = self._input_choice("(1/2): ", ["1", "2"])
        
        if choice == "1":
            nodes = self._input_nodes_manually()
        else:
            nodes = self._generate_uniform_nodes()

        self.functions.register_polynomial(self.N)

        print("\n  Итоговый набор узлов:")
        for i, x in enumerate(nodes):
            print(f"    x[{i+1}] = {x:.10f}")

        self._build_quadrature(nodes)


    def _input_nodes_manually(self) -> list:
        print(f"\n  Введите {self.N} узлов:")
        nodes = []
        for i in range(self.N):
            while True:
                x = self._input_float(f"    x[{i+1}] = ")
                if x not in nodes:
                    nodes.append(x)
                    break
                print("    [!] Узлы должны быть попарно различны. Повторите ввод.")
        return nodes


    def _generate_uniform_nodes(self) -> list:
        if self.N == 1:
            nodes = [(self.a + self.b) / 2.0]
        else:
            h = (self.b - self.a) / (self.N - 1)
            nodes = [self.a + i * h for i in range(self.N)]
        
        print(f"\n  Сгенерированы равноотстоящие узлы (h = {h:.10f}):" if self.N > 1 else 
            "\n  Сгенерирован узел в середине отрезка:")
        for i, x in enumerate(nodes):
            print(f"    x[{i+1}] = {x:.10f}")
        
        return nodes
    
    def _build_quadrature(self, nodes: list) -> None:
        print("\n" + "-" * 40)
        print("  Построение ИКФ")
        print("-" * 40)
        
        breakpoints = self.weight.get_breakpoints()
        self.moments = Moments(self.a, self.b, self.weight.calculate, breakpoints)
        
        self.quadrature = Quadrature()
        self.quadrature.build(self.N, nodes, self.a, self.b, self.moments)
        
        print("\n  Вычислены моменты веса:")
        for m in range(self.N):
            mu = self.moments.compute(m)
            print(f"    μ_{m} = {mu:.12f}")
        print(self.quadrature.print_info(self.functions))

        self._check_accuracy()
        
        self.integrals = Integrals(self.a, self.b, self.functions, self.weight.calculate)
        self.integrals.compute_all()
    
    def _check_accuracy(self) -> None:
        print("\n  Проверка точности на многочлене степени N-1 (f4):")

        _, f4_func = self.functions.get_function("f4")

        exact_f4 = self.moments.compute(self.N - 1) + self.moments.compute(0)
        approx_f4 = self.quadrature.integrate(f4_func)
        diff = abs(exact_f4 - approx_f4)
        
        print(f"    Точное значение:    {exact_f4:.15f}")
        print(f"    Приближённое:        {approx_f4:.15f}")
        print(f"    Разность:            {diff:.2e}")
    
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
 
        approx = self.quadrature.integrate(func)

        exact = self.integrals.get_exact(self.selected_func_key)

        abs_err = abs(exact - approx)
        rel_err = abs_err / abs(exact) if abs(exact) > 1e-15 else abs_err
        
        print(f"  Функция: {self.functions.get_name(self.selected_func_key)}")
        print(f"  Приближённое значение: {approx:.15f}")
        print(f"  Точное значение:       {exact:.15f}")
        print(f"  Абсолютная погрешность: {abs_err:.2e}")
        print(f"  Относительная погрешность: {rel_err:.2e} ({rel_err*100:.6f}%)")
    
    def run(self) -> None:
        self._dialog_greeting()
        
        self.functions = Functions()
        
        self._dialog_interval()
        self._dialog_nodes()
        self._dialog_select_function()
        self._dialog_compute()
        self._first_run = False
        
        while True:
            print("\n" + "=" * 55)
            print("  [1] Выбрать другую функцию")
            print("  [2] Ввести новые узлы (и N)")
            print("  [3] Изменить границы [a, b]")
            print("  [4] Повторить вычисление для текущей функции")
            print("  [0] Выход")
            print("=" * 55)
            
            choice = self._input_choice("  Ваш выбор: ", ["0", "1", "2", "3", "4"])
            
            if choice == "0":
                print("\n  Программа завершена.")
                break
            
            elif choice == "1":
                self._dialog_select_function()
                self._dialog_compute()
            
            elif choice == "2":
                self._dialog_nodes()
                self._dialog_select_function()
                self._dialog_compute()
            
            elif choice == "3":
                self._dialog_interval()
                if self.moments:
                    self.moments.clear_cache()
                print("\n  [!] Требуется ввести новые узлы для новых границ.")
                self._dialog_nodes()
                self._dialog_select_function()
                self._dialog_compute()
            
            elif choice == "4":
                self._dialog_compute()
            
            print()