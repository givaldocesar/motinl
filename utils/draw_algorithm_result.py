def draw_algorithm_result(x_final, z_final, method, canvas_contour, canvas_surface):
    x = x_final[0]
    y = x_final[1] if len(x_final) > 1 else 0.0
    z = z_final

    marker_config = {
        'marker': '*',                
        'markersize': 18,              
        'color': method.color,          
        'markeredgecolor': 'black',    
        'markeredgewidth': 1.5,       
        'zorder': 10, 
        'label': method.display_name             
    }

    canvas_contour.axes.plot([x], [y], **marker_config)
    canvas_contour.axes.legend(loc='upper right')
    canvas_contour.canvas.draw()
    canvas_surface.axes.plot([x], [y], [z], **marker_config)
    canvas_surface.axes.legend(loc='upper right')
    canvas_surface.canvas.draw()