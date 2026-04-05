from UserInt import UserInterface
from Functions import Function1, Function2, Function3, Function4

if __name__ == "__main__":
    test_funcs = [Function1(), Function2(), Function3(), Function4()]
    
    ui = UserInterface(test_funcs)
    ui.run()