import numpy as np
import sympy as sp
from utils import evaluate_f
from .armijo import armijo


def gradiente(func, expression, var_x, var_y, data):
    """
        Executa o método do Gradiente.
        
        Parâmetros:
        func: Função NumPy gerada pelo lambdify.
        data: Dicionário com as seguintes chaves =>
            -x0: Lista ou array com o ponto inicial [x, y].
            -alpha_inicial: Tamanho do passo inicial.
            -tolerance: Tolerância (critério de parada para o passo).
            -max_iterations: Número máximo de iterações permitidas.
        
        Retorna:
        ponto_minimo (array), historico (lista de dicionários para a tabela)
    """
    x_current = np.array(data["x0"], dtype=float)
    f_current = evaluate_f(func, x_current)
    alpha = data["alpha"]
    max_iterations = data["max_iterations"]
    tolerance = data["tolerance"]
    optimization_type = data['optimization_type']
    
    #Calcula o gradiente
    diff_x = sp.diff(expression, var_x)
    diff_y = sp.diff(expression, var_y)
    gradient = sp.lambdify((var_x, var_y), [diff_x, diff_y], modules=['numpy'])

    iteration = 1

    while max_iterations == 0 or iteration <= max_iterations:
        if(iteration > max(10000, max_iterations)):
            break
        
        x_val = x_current[0]
        y_val = x_current[1] if len(x_current) > 1 else 0.0

        # 1. Calcula o gradiente 
        vector = gradient(x_val, y_val)
        grad_vector = np.array(vector, dtype=float)

        if len(x_current) == 1:
            grad_vector = grad_vector[:1]
        
        grad_norm = np.linalg.norm(grad_vector)

        #Encerra se o tamanho do vetor gradiente é menor q a tolerância
        if grad_norm < tolerance:
            break
            
        if optimization_type == 'max':
            direction = grad_vector
        else:
            direction = -grad_vector
        
        # 2. Segue apra o próximo ponto na direção do gradiente
        x_start = x_current.copy()
        f_start = f_current

        alpha_k = armijo(x_current, func, alpha, grad_vector, direction, optimization_type)

        x_next = x_current + (alpha_k * direction)
        f_next = evaluate_f(func, x_next)

        # Prepara a linha da tabela
        if len(x_current) > 1:
            str_xk = f"[{x_current[0]:.6f}, {x_current[1]:.6f}]"
            str_grad = f"[{grad_vector[0]:.6f}, {grad_vector[1]:.6f}]"
        else:
            str_xk = f"[{x_current[0]:.6f}]"
            str_grad = f"[{grad_vector[0]:.6f}]"
        
        str_alpha_k = f"{alpha_k:.6f}"           
        table_row = [str(iteration), str_xk, f"{f_current:.6f}", str_grad, str_alpha_k]

        yield {
            "table_row": table_row,
            "x_start": x_start,
            "x_end": x_next,
            "z_start": f_start,
            "z_end": f_next,
            "status": "Aceito",
            "x_final": x_next,
            "z_final": f_next
        }

        x_current = x_next
        f_current = f_next
        iteration += 1