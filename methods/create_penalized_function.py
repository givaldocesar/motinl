import sympy as sp
from utils import is_valid_vars

def create_penalized_function(equation_expression, var_x, var_y, restrictions_str=[], weight=10000):
    penalty_expression = equation_expression
    allowed_vars = {var_x, var_y}

    for restrict_str in restrictions_str:
        
        if "=" in restrict_str and "==" not in restrict_str and "<=" not in restrict_str and ">=" not in restrict_str:
            restrict_str = restrict_str.replace("=", "==")

        relationship = is_valid_vars(equation_expression, allowed_vars, restrict_str)

        if hasattr(relationship, 'lhs') and hasattr(relationship, 'rhs'):
            lhs = relationship.lhs
            rhs = relationship.rhs

            if isinstance(relationship, sp.core.relational.Equality):
                penalty = (lhs - rhs)**2
            elif isinstance(relationship, (sp.core.relational.LessThan, sp.core.relational.StrictLessThan)):
                g_expr = lhs - rhs
                penalty = sp.Piecewise((g_expr**2, g_expr > 0), (0, True))
            elif isinstance(relationship, (sp.core.relational.GreaterThan, sp.core.relational.StrictGreaterThan)):
                g_expr = rhs - lhs
                penalty = sp.Piecewise((g_expr**2, g_expr > 0), (0, True))
        
        else:
            g_expression = relationship
            penalty = sp.Piecewise((g_expression**2, g_expression > 0), (0, True))
        
        penalty_expression += weight * penalty
    
    p = sp.lambdify((var_x, var_y), penalty_expression, modules=['numpy'])

    return p, penalty_expression