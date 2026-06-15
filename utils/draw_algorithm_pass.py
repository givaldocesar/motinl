def draw_algorithm_pass(data, method, canvas_contour, canvas_surface, force_draw=True):
    x0 = data["x_start"][0]
    y0 = data["x_start"][1] if len(data["x_start"]) > 1 else 0.0
    x1 = data["x_end"][0]
    y1 = data["x_end"][1] if len(data["x_end"]) > 1 else 0.0

    z0 = data["z_start"]
    z1 = data["z_end"]

    if data["status"] == "Aceito":
        marker_config = {
            'marker': 'o',
            'linestyle': '-',
            'linewidth': 2,                
            'markersize': 4,              
            'color': method.color, 
            'zorder': 10                         
        }
    
        canvas_contour.axes.plot([x0, x1], [y0, y1], **marker_config)
        canvas_surface.axes.plot([x0, x1], [y0, y1], zs=[z0, z1], **marker_config)

        if(force_draw):
            canvas_contour.canvas.draw()    
            canvas_surface.canvas.draw()
