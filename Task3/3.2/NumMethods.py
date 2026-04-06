from Functions import TestFunction

class NumericalMethods:
    def __init__(self, y_values, h):
        self.y = y_values
        self.h = h
        self.m = len(y_values) - 1

    def get_first_derivative_oh2(self):
        df = [0.0] * (self.m + 1)
        h = self.h
        y = self.y

        for k in range(self.m + 1):
            if k == 0:
                df[k] = (-3*y[0] + 4*y[1] - y[2]) / (2 * h)
            elif k == self.m:
                df[k] = (3*y[self.m] - 4*y[self.m-1] + y[self.m-2]) / (2 * h)
            else:
                df[k] = (y[k+1] - y[k-1]) / (2 * h)
        return df

    def get_first_derivative_oh4(self):
            if self.m < 4:
                return [None] * (self.m + 1)

            df = [0.0] * (self.m + 1)
            h = self.h
            y = self.y
            
            for k in range(self.m + 1):
                if k == 0:
                    df[k] = (-25*y[0] + 48*y[1] - 36*y[2] + 16*y[3] - 3*y[4]) / (12 * h)
                elif k == 1:
                    df[k] = (-3*y[0] - 10*y[1] + 18*y[2] - 6*y[3] + y[4]) / (12 * h)
                elif 2 <= k <= self.m - 2:
                    df[k] = (y[k-2] - 8*y[k-1] + 8*y[k+1] - y[k+2]) / (12 * h)
                elif k == self.m - 1:
                    df[k] = (3*y[self.m] + 10*y[self.m-1] - 18*y[self.m-2] + 6*y[self.m-3] - y[self.m-4]) / (12 * h)
                elif k == self.m:
                    df[k] = (25*y[self.m] - 48*y[self.m-1] + 36*y[self.m-2] - 16*y[self.m-3] + 3*y[self.m-4]) / (12 * h)
            return df

    def get_second_derivative_oh2(self):
        if self.m < 3:
            return [None] * (self.m + 1)
        
        ddf = [0.0] * (self.m + 1)
        h2 = self.h ** 2
        y = self.y

        for k in range(self.m + 1):
            if k == 0:
                ddf[k] = (2*y[0] - 5*y[1] + 4*y[2] - y[3]) / h2
            elif k == self.m:
                ddf[k] = (2*y[self.m] - 5*y[self.m-1] + 4*y[self.m-2] - y[self.m-3]) / h2
            else:
                ddf[k] = (y[k+1] - 2*y[k] + y[k-1]) / h2
        return ddf
    
    def find_optimal_step(self, func_obj: TestFunction, x_point, initial_h=0.1):
        results = []
        h = initial_h
        prev_error = float('inf')

        exact_df = func_obj.df(x_point)
        
        for _ in range(100):
            y0 = round(func_obj.f(x_point), 5)
            yh = round(func_obj.f(x_point + h), 5)
            y2h = round(func_obj.f(x_point + 2*h), 5)
            
            approx_df = (-3*y0 + 4*yh - y2h) / (2 * h)
            error = abs(exact_df - approx_df)
            
            results.append((h, exact_df, approx_df, error))
            
            if error > prev_error:
                break
            prev_error = error
            h /= 2
            
        return results