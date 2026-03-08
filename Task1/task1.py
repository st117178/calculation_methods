import math
import random
from tabulate import tabulate

def root_sep():
    while True:
        try:
            A = float(input("Введите значение A: "))
            B = float(input("Введите значение B: "))
            if A >= B:
                print("Введенные значения A и B, не корректны A >= B. Попробуйте еще раз.")
                continue
            break
        except:
            print("Введенные значения не корректны. Убедитесь, что A, B число.")

    segments = []
    while True:
        try:
            N = int(round(float(input("Введите значение N >= 2: "))))
            if N < 2:
                print("Введенное значение N, не корректны N < 2. Попробуйте еще раз.")
                continue
        except:
            print("Введенные значения не корректны. Убедитесь, что N число.")
    
        H = (B - A) / N

        x1 = A
        x2 = x1 + H
        y1 = f(x1)

        while x2 <= B:
            y2 = f(x2)
            if y1 * y2 <= 0:
                segments.append([x1, x2])

            x1 = x2
            x2 = x1 + H
            y1 = y2

        print(f"Найдено {len(segments)} отрезков перемены знака с шагом {H = }:")
        for i, segment in enumerate(segments):
            print(f"{i}: {segment}")

        y_n = input(f"Хотите поменять {N = }? y/n: ")

        if y_n == "y":
            continue
        else:
            break
    return segments


def claryfying_roots(segments: list, list_func=None):
    while True:
        i = 0
        while True:
            try:
                print(f"Выбор отрезка из:")
                for k, segment in enumerate(segments):
                    print(f"{k}: {segment}")
                i = int(input(f"Введите номер отрезка i от 0 до {len(segments) - 1}: "))
                if not (0 <= i <= len(segments) - 1):
                    print(f"Введенное значение {i = }, не корректно. Попробуйте еще раз.")
                    continue
                break
            except:
                print(f"Введенное значение не корректно. Убедитесь, что {i = } число.")
        E = 0
        while True:
            try:
                E = float(input("Введите значение E > 0: "))
                if E <= 0:
                    print(f"Введенное значение {E = }, не корректно E <= 0. Попробуйте еще раз.")
                    continue
                break
            except:
                print(f"Введенное значение не корректно. Убедитесь, что {E = } число.")
        
        if list_func is None:
            list_func = [bis_method, newton_method, mod_newton_method, secant_method]
            data = printer_methods(list_func, E, segments[i], True)
        else:
            data = printer_methods(list_func, E, segments[i])

        j = 0
        while True:
            try:
                choise_list = [
                    "Продолжить уточнение других отрезков.",
                    "Перейти к каталогу задач."
                ]
                print(f"Выбирите пункт:")
                for k, choise in enumerate(choise_list):
                    print(f"{k}: {choise}")
                j = int(input(f"Введите номер пункта {len(choise_list) - 1}: "))
                if not (0 <= j <= len(choise_list) - 1):
                    print(f"Введенное значение {j = }, не корректно. Попробуйте еще раз.")
                    continue
                break
            except:
                print(f"Введенное значение не корректно. Убедитесь, что {j = } число.")

        if j != 0:
            return data


def bis_method(E: float, segment: list):
    a = segment[0]
    b = segment[1]

    counter = 0
    while b - a > 2 * E:
        c = (a + b) / 2
        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c
        counter += 1
    
    x = (a + b) / 2

    last_interval_length = b - a

    delta = (b - a) / 2

    residual = abs(f(x))

    dict_data = {
        "Название метода": "Метод биссекций",
        "Начальное приближение": segment,
        "Количество шагов": counter,
        "Приближенное решение x": x,
        "Длина последнего отрезка": last_interval_length,
        "Модуль невязки": residual,
        "Δ(для биссекции)": delta
    }

    return dict_data


def newton_x_k(x_k_minus_1: float):
    return x_k_minus_1 - f(x_k_minus_1) / df(x_k_minus_1)


def newton_method(E: float, segment: list):
    x0 = 0
    list_x0 = [
        segment[0],
        segment[1],
        (segment[1] + segment[0]) / 2,
        random.uniform(segment[0], segment[1])
    ]
    for x in list_x0:
        if f(x) * d2f(x) > 0:
            x0 = x
            break
        x0 = x
    
    counter = 0
    x_k_minus_1 = x0
    x_k = newton_x_k(x_k_minus_1)
    counter += 1

    while abs(x_k - x_k_minus_1) >= E:
        x_k_minus_1 = x_k
        x_k = newton_x_k(x_k_minus_1)
        counter += 1

    last_lenght = abs(x_k - x_k_minus_1)
    residual = abs(f(x_k))

    dict_data = {
        "Название метода": "Метод Ньютона",
        "Начальное приближение": x0,
        "Количество шагов": counter,
        "Приближенное решение x": x_k,
        "Длина последнего отрезка": last_lenght,
        "Модуль невязки": residual,
        "Δ(для биссекции)": None
    }

    return dict_data


def mod_newton_x_k(x_k_minus_1: float, x0: float):
    return x_k_minus_1 - f(x_k_minus_1) / df(x0)


def mod_newton_method(E: float, segment: list):
    x0 = 0
    list_x0 = [
        segment[0],
        segment[1],
        (segment[1] + segment[0]) / 2,
        random.uniform(segment[0], segment[1])
    ]
    for x in list_x0:
        if f(x) * d2f(x) > 0:
            x0 = x
            break
        x0 = x
    
    counter = 0
    x_k_minus_1 = x0
    x_k = mod_newton_x_k(x_k_minus_1, x0)
    counter += 1

    while abs(x_k - x_k_minus_1) >= E:
        x_k_minus_1 = x_k
        x_k = mod_newton_x_k(x_k_minus_1, x0)
        counter += 1

    last_lenght = abs(x_k - x_k_minus_1)
    residual = abs(f(x_k))

    dict_data = {
        "Название метода": "Модифицированный метод Ньютона",
        "Начальное приближение": x0,
        "Количество шагов": counter,
        "Приближенное решение x": x_k,
        "Длина последнего отрезка": last_lenght,
        "Модуль невязки": residual,
        "Δ(для биссекции)": None
    }

    return dict_data


def secant_method_x_k(x_k_minus_1: float, x_k_minus_2: float):
    return x_k_minus_1 - f(x_k_minus_1) / (f(x_k_minus_1) - f(x_k_minus_2)) * (x_k_minus_1 - x_k_minus_2)


def secant_method(E: float, segment: list):
    x0 = segment[0]
    x1 = segment[1]

    counter = 0
    x_k_minus_1 = x1
    x_k_minus_2 = x0
    x_k = secant_method_x_k(x_k_minus_1, x_k_minus_2)
    counter += 1

    while abs(x_k - x_k_minus_1) >= E and abs(f(x_k)) >= E:
        x_k_minus_2 = x_k_minus_1
        x_k_minus_1 = x_k
        x_k = secant_method_x_k(x_k_minus_1, x_k_minus_2)
        counter += 1

    last_lenght = abs(x_k - x_k_minus_1)
    residual = abs(f(x_k))

    dict_data = {
        "Название метода": "Метод секущих",
        "Начальное приближение": [x0, x1],
        "Количество шагов": counter,
        "Приближенное решение x": x_k,
        "Длина последнего отрезка": last_lenght,
        "Модуль невязки": residual,
        "Δ(для биссекции)": None
    }

    return dict_data


def printer_methods(func_list: list[callable], e, segment, is_print=False):
    dict_list_data = []
    for func in func_list:
        dict_data_func = func(e, segment)
        dict_list_data.append(dict_data_func)
    if is_print:
        print(tabulate(
            dict_list_data,
            headers="keys",
            tablefmt="grid",
            floatfmt=(".16f", ".16f", ".16f", ".16f"),
            missingval="—"
            ))


def f(x: float):
    return 10*math.cos(x) - 0.1*x**2

def df(x: float):
    return (-10)*math.sin(x) - 0.2*x


def d2f(x: float):
    return (-10)*math.cos(x) - 0.2


def ball_task():
    materials_dict = {
        "Пробка": 0.25,
        "Бамбук": 0.4,
        "Сосна (белая)": 0.5,
        "Кедр": 0.55,
        "Дуб": 0.7,
        "Бук": 0.75,
        "Красное дерево": 0.8,
        "Тиковое дерево": 0.85,
        "Парафин": 0.9,
        "Лёд/Полиэтилен": 0.92,
        "Пчелиный воск": 0.95
    }
    
    while True:
        try:
            r = float(input("Введите радиус шара в метрах: "))
            if r <= 0:
                print("Радиус должен быть положительным числом. Попробуйте еще раз.")
                continue
            
            print(f"Задача о погружении шара")
            print(f"Радиус шара: {r} м")
            
            results = []
            
            for material, density in materials_dict.items():
                def f_ball(d):
                    return math.pi/3 * (d**3 - 3*d**2*r + 4*r**3*density)
                def df_ball(d):
                    return math.pi/3 * (3*d**2 - 6*d*r)
                def d2f_ball(d):
                    return math.pi/3 * (6*d - 6*r)
                
                global f, df, d2f
                original_f = f
                original_df = df
                original_d2f = d2f

                f = f_ball
                df = df_ball
                d2f = d2f_ball

                segment = [0.0, 2*r]

                if f(segment[0]) * f(segment[1]) > 0:
                    depth = None
                    steps = 0
                    residual = None
                    last_diff = None
                else:
                    result = secant_method(1e-8, segment)
                    depth = result["Приближенное решение x"]
                    steps = result["Количество шагов"]
                    residual = result["Модуль невязки"]
                    last_diff = result["Длина последнего отрезка"]
                    
                    if depth < 0 or depth > 2*r:
                        depth = None
                        steps = 0
                        residual = None
                        last_diff = None
                
                results.append({
                    "Материал": material,
                    "Плотность ρ, г/мл": density,
                    "Глубина погружения d, м": depth if depth is not None else "—",
                    "Кол-во итераций": steps if steps > 0 else "—",
                    "Невязка |f(d)|": f"{residual:.2e}" if residual is not None else "—"
                })
                
                f = original_f
                df = original_df
                d2f = original_d2f
            
            print(tabulate(
                results,
                headers="keys",
                tablefmt="grid",
                floatfmt=(".2f", ".2f", ".16f", "d"),
                missingval="—"
            ))
            
            choice = input("Рассчитать для другого радиуса? (y/n): ").lower()
            if choice != 'y':
                break
                
        except:
            print("Ошибка: введите корректное число.")

if __name__ == "__main__":
    ballon_task_dict = {
        "Пробка": 0.25,
        "Бамбук": 0.4,
        "Сосна (белая)": 0.5,
        "Кедр": 0.55,
        "Дуб": 0.7,
        "Бук": 0.75,
        "Красное дерево": 0.8,
        "Тиковое дерево": 0.85,
        "Парафин": 0.9,
        "Лёд/Полиэтилен": 0.92,
        "Пчелиный воск": 0.95
    }
    j = 0
    while True:
        while True:
            try:
                choise_list = [
                    "Выход.",
                    "Задача по поиску корней функции f(x) = 10 ∙ cos(x) ‒ 0,1 ∙ x^2. Условия [A, B] = [‒8; 2], ε = 10-5",
                    "Задача про шар."
                ]
                print(f"Выбирите пункт:")
                for k, choise in enumerate(choise_list):
                    print(f"{k}: {choise}")
                j = int(input(f"Введите номер пункта: "))
                if not (0 <= j <= len(choise_list) - 1):
                    print(f"Введенное значение {j = }, не корректно. Попробуйте еще раз.")
                    continue
                break
            except:
                print(f"Введенное значение не корректно. Убедитесь, что {j = } число.")

        if j == 0:
            break  
        elif j == 1:
            segments = root_sep()
            claryfying_roots(segments)
        else:
            ball_task()
        