import sympy as sp

def is_valid_vars(equation_expression, allowed_vars, restrict_str):
    relationship = sp.sympify(restrict_str)
    rlt_vars = relationship.free_symbols
        
    if not rlt_vars.issubset(allowed_vars):
        raise ValueError(f"A restrição {restrict_str} possui variáveis diferentes da função objetivo ({equation_expression}).")

    return relationship