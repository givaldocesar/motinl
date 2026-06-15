import numpy as np
from utils.evaluate_f import evaluate_f

def armijo(x, f, base_alpha, gradient, direction, optimization_type = 'min'):
    alpha_k = base_alpha
    reduction_factor = 0.5
    c = 0.0001                  # Amortecimento

    # produto interno do gradiente com a direção
    grad_dot_dir = np.dot(gradient, direction)

    while alpha_k > 1e-8:
        f_current = evaluate_f(f, x)
        x_possible = x + (alpha_k * direction)
        f_possible = evaluate_f(f, x_possible)

        # Desigualdade de armijo
        if optimization_type == 'max':
            if f_possible >= f_current + (c * alpha_k * grad_dot_dir):
                break 
        else:
            if f_possible <= f_current + (c * alpha_k * grad_dot_dir):
                break
        
        alpha_k = alpha_k * reduction_factor

    return alpha_k