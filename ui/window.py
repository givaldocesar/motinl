from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
                             QMessageBox, QTableWidgetItem)

from ui.configs_area import ConfigsArea
from ui.iteration_table import TableArea
from ui.canvas import Canvas
from controllers import Process, EVENTS
from utils import (plot_graphs, draw_algorithm_pass, draw_algorithm_result)
from methods import Methods

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MOTINL - Métodos de Otimização Não Linear")
        self.resize(1280, 720)
        self.create_ui()

        self.process = Process()

        self.process.on(EVENTS.PLOT_GRAPHS, self.update_canvas)
        self.process.on(EVENTS.INSERT_TABLE_ROW, self.table_area.insert_row)
        self.process.on(EVENTS.DRAW_METHODS, self.draw_methods)
        self.process.on(EVENTS.STEP_EXECUTED, self.on_step_executed)

        self.method_changed()
        self.showMaximized()

    def create_ui(self):
        self.setCentralWidget(QWidget())
        main_layout = QHBoxLayout(self.centralWidget())
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        #Configs Panel
        self.configs_area = ConfigsArea(self)
        self.configs_area.equation_preview.clicked.connect(self.show_preview)
        self.configs_area.input_method.currentTextChanged.connect(self.method_changed)
        self.configs_area.run_btn.clicked.connect(self.run)
        self.configs_area.stop_btn.clicked.connect(self.stop)
        splitter.addWidget(self.configs_area)
        
        canvas_widget = QWidget()
        canvas_layout = QVBoxLayout(canvas_widget)
        self.canvas_contour = Canvas(self, width=5, height=4, dpi=100, title="Curvas de Nível")
        canvas_layout.addWidget(self.canvas_contour)

        self.canvas_surface = Canvas(self, width=5, height=4, dpi=100, is_3d=True, title="Gráfico da função")
        canvas_layout.addWidget(self.canvas_surface)

        splitter.addWidget(canvas_widget)
        
        self.table_area = TableArea(self)
        splitter.addWidget(self.table_area)
        splitter.setSizes([300,400,580])

    def show_preview(self):
        data = self.configs_area.get_data()
        self.update_canvas({
            "expression": data["expression"],
            "center": data["x0"]
        })

    def draw_methods(self, data):
        historic, is_running, current_method = data.values()
        
        for method, steps in historic.items():
            for step in steps:
                draw_algorithm_pass(
                    step, 
                    method, 
                    self.canvas_contour, 
                    self.canvas_surface, 
                    force_draw=False
                )
            
            if steps[-1]["x_final"] is not None and is_running and current_method != method:
                draw_algorithm_result(steps[-1]["x_final"], steps[-1]["z_final"], method, self.canvas_contour, self.canvas_surface)
                
        self.canvas_contour.canvas.draw()
        self.canvas_surface.canvas.draw()

        QApplication.processEvents()
    
    def draw_result_on_table(self, str_x_opt, str_z_opt):
        num_cols = self.table_area.table.columnCount()
        result_row = ["RESULTADO", str_x_opt, str_z_opt]

        while len(result_row) < num_cols:
            result_row.append("----")

        row_idx = self.table_area.table.rowCount()
        self.table_area.table.insertRow(row_idx)

        for col_idx, texto in enumerate(result_row):
            item = QTableWidgetItem(texto)
            item.setForeground(QColor("#D32F2F")) 
            
            fonte = item.font()
            fonte.setBold(True)
            item.setFont(fonte)

            self.table_area.table.setItem(row_idx, col_idx, item)
        
        self.table_area.table.scrollToBottom()

    def on_step_executed(self, step):
        method = step["method"]
        draw_algorithm_pass(step["data"], method, self.canvas_contour, self.canvas_surface)

        row_idx = self.table_area.table.rowCount()
        if row_idx % 5 == 0: 
            self.table_area.table.scrollToBottom()
        
        QApplication.processEvents()

    def update_canvas(self, data):
        if(data["expression"]):
            plotted, message = plot_graphs(
                equation_string=data["expression"],
                canvas_contour=self.canvas_contour,
                canvas_surface=self.canvas_surface,
                center=data["center"],
                penalty_string=None if not "penalty_expression" in data else data["penalty_expression"],
                radius=10.0 if 'radius' not in data else data["radius"]
            )

            if not plotted:
                QMessageBox.critical(self, "Erro ao processar equação", message)
        
        QApplication.processEvents()  
    
    def method_changed(self):
        method = self.configs_area.input_method.currentData()
        historic = self.process.get_global_historic(method)

        self.table_area.update_table_headers(method)

        if historic and len(historic) > 0:
            for step_data in historic:
                self.table_area.insert_row(step_data["table_row"])
            
            x_opt = historic[-1]["x_final"]
            z_opt = historic[-1]["z_final"]

            str_x_opt = f"[{x_opt[0]:.6f}, {x_opt[1]:.6f}]" if len(x_opt) > 1 else f"[{x_opt[0]:.6f}]"
            str_z_otp = f"{z_opt:.6f}"
            
            self.draw_result_on_table(str_x_opt, str_z_otp)
            self.table_area.table.scrollToBottom()
        
        QApplication.processEvents()  

    def stop(self):
        self.process.set_running(False)

    def run(self):
        self.configs_area.enable_ui(False)
        self.table_area.table.setRowCount(0)

        data = self.configs_area.get_data()
        self.process.set_data(data)
        is_ok, message = self.process.run()

        if is_ok:
            method = data["method"]
            historic = self.process.get_global_historic(method)
            
            if historic and len(historic) > 0:
                last_step = historic[-1]
                draw_algorithm_result(last_step["x_final"], last_step["z_final"], method, self.canvas_contour, self.canvas_surface)
                self.canvas_contour.canvas.draw()
                self.canvas_surface.canvas.draw()
                
                x_opt = last_step["x_final"]
                z_opt = last_step["z_final"]

                str_x_opt = f"[{x_opt[0]:.6f}, {x_opt[1]:.6f}]" if len(x_opt) > 1 else f"[{x_opt[0]:.6f}]"
                str_z_otp = f"{z_opt:.6f}"
                
                result_message = (
                    f"Otimização Concluída com Sucesso!\n\n"
                    f"Ponto Ótimo (X*): {str_x_opt}\n"
                    f"Valor da Função f(X*): {str_z_otp}\n"
                    f"Total de Iterações: {len(historic)}"
                )

                if data["fast_mode"]:
                    for step_data in historic:
                        self.table_area.insert_row(step_data["table_row"])

                    self.draw_methods({
                        "historic": self.process.get_global_historic(), 
                        "is_running": False, 
                        "current_method": data["method"]
                    })

                self.draw_result_on_table(str_x_opt, str_z_otp)
                print(result_message)
                QMessageBox.information(self, "Resultado Final", result_message)
            else:
                QMessageBox.information(self, "Concluído", "O ponto inicial já é o ótimo!")
        else:
            print(message)
            QMessageBox.critical(self, "Erro de Processamento", message)
        
        self.configs_area.enable_ui(True)
 