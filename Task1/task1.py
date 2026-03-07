import math


def f(x: int):
    return 10 * math.cos(x) - 0.1 * x ** 2


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

def claryfying_roots(segments: list):
    i = 0
    while True:
        try:
            i = int(input(f"Введите номер отрезка i от 0 до {len(segments) - 1}: "))
            if not (0 <= i <= len(segments) - 1):
                print(f"Введенное значение {i = }, не корректно. Попробуйте еще раз.")
                continue
            break
        except:
            print(f"Введенное значение не корректно. Убедитесь, что {i = } число.")

    while True:
        try:
            E = float(input("Введите значение E > 0: "))
            if E <= 0:
                print(f"Введенное значение {E = }, не корректно E <= 0. Попробуйте еще раз.")
                continue
            break
        except:
            print(f"Введенное значение не корректно. Убедитесь, что {E = } число.")

    return bis_method(E, segments[i])

    
def bis_method(E: float, segment: list):
    a = segment[0]
    b = segment[1]

    counter = 0
    while b - a > 2 * E:
        c = (a + b) / 2
        if f(a) * f(b) <= 0:
            b = c
        else:
            a = c
        counter += 1
    
    x = (a + b) / 2
    delta = (b - a) / 2

    return counter, x, delta



def newton_method(E: float, segment: list):
    ...

def mod_newton_method(E: float, segment: list):
    ...

def secant_method(E: float, segment: list):
    ...

if __name__ == "__main__":
    print(f(-4.961500976561485))
    segments = root_sep()
    print(claryfying_roots(segments))