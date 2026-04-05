from Functions import TestFunction

class DataManager:
    def __init__(self, test_function: TestFunction):
        self.func_obj = test_function
        self.x_nodes = []            
        self.y_values = []           
        self.h = 0                   
        self.m = 0                   

    def generate_table(self, x0, h, m):
        self.h = h
        self.m = m

        self.x_nodes = [x0 + k * h for k in range(m + 1)]
        
        self.y_values = [self.func_obj.f(x) for x in self.x_nodes]
        
        return self.x_nodes, self.y_values

    def get_exact_derivatives(self):
        df_exact = [self.func_obj.df(x) for x in self.x_nodes]
        ddf_exact = [self.func_obj.ddf(x) for x in self.x_nodes]
        return df_exact, ddf_exact

    def get_node_count(self):
        return len(self.x_nodes)