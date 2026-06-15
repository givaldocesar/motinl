from PyQt6.QtWidgets import * 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Canvas(QWidget):
    def __init__(self, parent=None, width=5, height=4, dpi=100, is_3d=False, title=""):
        super().__init__(parent)
        self.setLayout(QVBoxLayout(self))

        figure = Figure(figsize=(width, height), dpi=dpi)

        if(is_3d):
            self.axes = figure.add_subplot(111, projection='3d')
        else:
            self.axes = figure.add_subplot(111)
        
        self.canvas = FigureCanvas(figure)
        self.canvas.setParent(self)
        self.axes.set_title(title)

        toolbar_contour = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(toolbar_contour)
        self.layout().addWidget(self.canvas)