import math

class TestFunction:
    def __init__(self, name):
        self.name = name

    def f(self, x):
        raise NotImplementedError
    
    def df(self, x):
        raise NotImplementedError
    
    def ddf(self, x):
        raise NotImplementedError

class Function1(TestFunction):
    def __init__(self):
        super().__init__("f1(x) = -3x^2 + 10x + 3")
    def f(self, x): return -3*x**2 + 10*x + 3
    def df(self, x): return -6*x + 10
    def ddf(self, x): return -6

class Function2(TestFunction):
    def __init__(self):
        super().__init__("f2(x) = 10x^3 - 3x^2 + 5")
    def f(self, x): return 10*x**3 - 3*x**2 + 5
    def df(self, x): return 30*x**2 - 6*x
    def ddf(self, x): return 60*x - 6

class Function3(TestFunction):
    def __init__(self):
        super().__init__("f3(x) = exp(2x)")
    def f(self, x): return math.exp(2*x)
    def df(self, x): return 2 * math.exp(2*x)
    def ddf(self, x): return 4 * math.exp(2*x)

class Function4(TestFunction):
    def __init__(self):
        super().__init__("f4(x) = sin(2x) - 1.25x^2 + 0.35")
    def f(self, x): 
        return math.sin(2*x) - 1.25*x**2 + 0.35
    def df(self, x): 
        return 2*math.cos(2*x) - 2.5*x
    def ddf(self, x): 
        return -4*math.sin(2*x) - 2.5