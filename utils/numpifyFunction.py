import sympy as sp

def numpifyFunction(equation_string):
    #converte a função para simbolos
    expression = sp.sympify(equation_string)
    
    #extrai as variáveis
    variables = list(expression.free_symbols)
    variables.sort(key=lambda v: v.name)

    if(len(variables) > 2):
        raise ValueError("O gráfico suporta no máximo 2 variáveis.")
    
    if(len(variables) == 0):
        raise ValueError("Nenhuma variável encontrada na equação.")

    #adiciona y caso não tenha
    x = variables[0]
    y = variables[1] if len(variables) == 2 else sp.Symbol('y')
    return sp.lambdify((x, y), expression, modules=['numpy']), expression, x, y
    