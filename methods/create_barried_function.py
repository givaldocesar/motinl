import sympy as sp

def create_barried_function(equation_expression, var_x, var_y, restrictions_str=[], weight=15):
    barried_expression = equation_expression
    allowed_vars = {var_x, var_y}

    for restrict_str in restrictions_str:
        
        if "=" in restrict_str and "==" not in restrict_str and "<=" not in restrict_str and ">=" not in restrict_str:
            restrict_str = restrict_str.replace("=", "==")

        relationship = sp.sympify(restrict_str)
        rlt_vars = relationship.free_symbols
        
        if not rlt_vars.issubset(allowed_vars):
            raise ValueError(f"A restrição {restrict_str} possui variáveis diferentes da função objetivo ({equation_expression}).")

        if hasattr(relationship, 'lhs') and hasattr(relationship, 'rhs'):
            lhs = relationship.lhs
            rhs = relationship.rhs

            if isinstance(relationship, sp.core.relational.Equality):
                raise ValueError("O Método das Barreiras requer um interior. Não é possível utilizar igualdades.")
            elif isinstance(relationship, (sp.core.relational.LessThan, sp.core.relational.StrictLessThan)):
                g_expr = lhs - rhs
                barrier = sp.Piecewise((-1 / g_expr, g_expr < 0), (1e10, True))
            elif isinstance(relationship, (sp.core.relational.GreaterThan, sp.core.relational.StrictGreaterThan)):
                g_expr = rhs - lhs
                barrier = sp.Piecewise((-1 / g_expr, g_expr < 0), (1e10, True))
        
        else:
            g_expression = relationship
            barrier = sp.Piecewise((-1 / g_expression, g_expression < 0), (1e10, True))
        
        barried_expression += weight * barrier
    
    b = sp.lambdify((var_x, var_y), barried_expression, modules=['numpy'])

    return b, barried_expression