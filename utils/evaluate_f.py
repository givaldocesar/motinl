def evaluate_f(func, point):
    if len(point) == 1:
        return func(point[0], 0.0)
    
    return func(*point)