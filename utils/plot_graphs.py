import numpy as np;
import sympy as sp;
from . import numpifyFunction

def plot_graphs(equation_string, canvas_contour, canvas_surface, resolution=100, center=None, radius=10.0, penalty_string=None,):
    expression_string = penalty_string if penalty_string else equation_string

    try:
        canvas_contour.axes.clear()
        canvas_surface.axes.clear()

        [func, expression, x, y] = numpifyFunction(expression_string)

        #Seta o ponto_inicial
        if center is not None and len(center) > 0:
            x_center = center[0]
            y_center = center[1] if len(center)> 1 else 0.0
        else:
            x_center, y_center = 0.0, 0.0
            
        # Malha numérica
        x_vals = np.linspace(x_center - radius, x_center + radius, resolution)
        y_vals = np.linspace(y_center - radius, y_center + radius, resolution)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = func(X, Y)

        if(np.isscalar(Z)):
            Z = np.full_like(X, Z)
        
        z_min = np.nanmin(Z)
        visual_edge = z_min + 500
        Z = np.clip(Z, a_min=None, a_max=visual_edge)

        raw_expr = sp.sympify(equation_string)
        raw_latex = sp.latex(raw_expr)

        # Curvas de nível
        canvas_contour.axes.contourf(X, Y, Z, levels=30, cmap='viridis', alpha=0.8)
        canvas_contour.axes.contour(X, Y, Z, levels=30, colors='k', linewidths=0.5)
        canvas_contour.axes.set_title(f"Curvas de Nível: ${raw_latex}$")
        canvas_contour.axes.set_xlabel(f"{x}")
        canvas_contour.axes.set_ylabel(f"{y}")
        canvas_contour.axes.grid(True, linestyle='--', alpha=0.5)

        canvas_surface.axes.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.9)
        canvas_surface.axes.set_title(f"Superfície: ${raw_latex}$")
        canvas_surface.axes.set_xlabel(f"{x}")
        canvas_surface.axes.set_ylabel(f"{y}")
        canvas_surface.axes.set_zlabel("f(x,y)")

        canvas_contour.canvas.draw()
        canvas_surface.canvas.draw()

        return (True, "")

    except Exception as e:
        message = f"Erro ao processar equação: {e}"
        print(message)
        return (False, message)