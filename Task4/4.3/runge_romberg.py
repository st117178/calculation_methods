class RungeRomberg:
    def __init__(self):
        pass

    @staticmethod
    def refine(j_h: float, j_h_l: float, l: int, ast: int) -> float:
        r = ast + 1
        l_r = l ** r
        return (l_r * j_h_l - j_h) / (l_r - 1)

    @staticmethod
    def get_order(ast: int) -> int:
        return ast + 1
