from User_Int import UserInterface
import math

def my_func(x):
    return math.exp(-x) - (x**2)/2

ui = UserInterface(func=my_func)
ui.run()