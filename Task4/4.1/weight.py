class Weight:
    def __init__(self):
        self._variant = 7
        self._description = "ρ(x) = |x - 0.5|"
    
    def calculate(self, x: float) -> float:
        return abs(x - 0.5)
    
    def get_description(self) -> str:
        return self._description
    
    def get_variant(self) -> int:
        return self._variant
    
    def has_singularity(self) -> bool:
        return False
    
    def get_breakpoints(self) -> list:
        return [0.5]