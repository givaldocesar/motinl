import sympy as sp
from methods import Methods
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QPushButton, 
                             QComboBox, QRadioButton, QPlainTextEdit, QLabel, QSpinBox, QDoubleSpinBox,
                             QCheckBox, QStyle)

class ConfigsArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_expression = None
        self.current_x0 = None
        self.setMaximumWidth(350)

        layout = QVBoxLayout(self)

        #Função Objetivo-----------------------------------------------
        function_group = QGroupBox("Função Objetivo f(x) ou f(x,y): ")
        equation_layout = QHBoxLayout(function_group)

        self.input_equation = QLineEdit()
        self.input_equation.setPlaceholderText("Ex: x**2 + y**2")
        self.input_equation.textChanged.connect(self.validate)
        equation_layout.addWidget(self.input_equation)

        self.equation_preview = QPushButton("🔍")
        self.equation_preview.setEnabled(False)
        self.equation_preview.setToolTip("Visualizar gráfico")
        self.equation_preview.setFixedWidth(30)
        equation_layout.addWidget(self.equation_preview)
        
        layout.addWidget(function_group)

        #Ponto Inicial-----------------------------------------------
        start_point_group = QGroupBox("Ponto Inicial X0: ")
        start_point_layout = QHBoxLayout(start_point_group)

        self.input_xo = QLineEdit()
        self.input_xo.setPlaceholderText("Ex: 1.0, -1.0")
        self.input_xo.textChanged.connect(self.validate)

        start_point_layout.addWidget(self.input_xo)

        layout.addWidget(start_point_group)

        #Métodos------------------------------------------------------
        methods_group = QGroupBox("Método de Otimização: ")
        methods_layout = QVBoxLayout(methods_group)

        self.input_method = QComboBox()
        methods_layout.addWidget(self.input_method)

        for method in Methods:
            self.input_method.addItem(method.display_name, userData=method)

        optimization_type_layout = QHBoxLayout()

        self.minimum_radio = QRadioButton("Minimizar")
        self.minimum_radio.setChecked(True)
        optimization_type_layout.addWidget(self.minimum_radio)

        self.maximum_radio = QRadioButton("Maximizar")
        optimization_type_layout.addWidget(self.maximum_radio)

        methods_layout.addLayout(optimization_type_layout)
        
        layout.addWidget(methods_group)
        
        #Métodos de restrição----------------------------------------
        restrictions_group  = QGroupBox("Método de Restrições")
        restriction_layout = QVBoxLayout(restrictions_group)

        restrict_opt_layout = QHBoxLayout()
        
        self.barrier_radio = QRadioButton("Barreiras")
        restrict_opt_layout.addWidget(self.barrier_radio)

        self.penalty_radio = QRadioButton("Penalidade")
        self.penalty_radio.setChecked(True)
        restrict_opt_layout.addWidget(self.penalty_radio)

        restriction_layout.addLayout(restrict_opt_layout)

        self.restrictions = QPlainTextEdit()
        self.restrictions.setPlaceholderText("Restrições (uma por linha):\nEx:\nx + y <= 5\nx >= 0")
        self.restrictions.setMinimumHeight(100)
        self.restrictions.setMaximumHeight(120)
        restriction_layout.addWidget(self.restrictions)

        layout.addWidget(restrictions_group)

        #Configurações de Iteração --------------------------------------
        configs_iteration_group = QGroupBox("Configurações de Iteração")    
        configs_iteration_layout = QVBoxLayout(configs_iteration_group)

        label_step_size = QLabel("Tamanho do passo (\u03B1): ")
        self.input_alpha = QDoubleSpinBox()
        self.input_alpha.setDecimals(4)       
        self.input_alpha.setMinimum(0.0001)   
        self.input_alpha.setMaximum(100.0)   
        self.input_alpha.setValue(0.1)
        self.input_alpha.setSingleStep(0.01)

        configs_iteration_layout.addWidget(label_step_size)
        configs_iteration_layout.addWidget(self.input_alpha)

        label_tolerance = QLabel("Tolerância (\u03B5): ")
        self.input_tolerance = QDoubleSpinBox()
        self.input_tolerance.setDecimals(6)
        self.input_tolerance.setMinimum(0.000001)
        self.input_tolerance.setMaximum(1.0)
        self.input_tolerance.setValue(0.0001)
        self.input_tolerance.setSingleStep(0.0001)

        configs_iteration_layout.addWidget(label_tolerance)
        configs_iteration_layout.addWidget(self.input_tolerance)

        label_max_iterations = QLabel("Máx. Iterações: ")
        self.input_max_iterations = QSpinBox()       
        self.input_max_iterations.setMinimum(0)     
        self.input_max_iterations.setMaximum(100000)
        self.input_max_iterations.setValue(0)

        configs_iteration_layout.addWidget(label_max_iterations)
        configs_iteration_layout.addWidget(self.input_max_iterations)

        layout.addWidget(configs_iteration_group)

        #Configurações de Execução---------------------------------------
        configs_execution_group = QGroupBox("Configurações de Execução")    
        configs_execution_layout = QVBoxLayout(configs_execution_group)

        self.hold_on = QCheckBox("Manter Gráfico entre métodos")
        self.hold_on.setChecked(True)
        configs_execution_layout.addWidget(self.hold_on)

        self.fast_mode = QCheckBox("Rodar no Background")
        self.fast_mode.setChecked(False)
        configs_execution_layout.addWidget(self.fast_mode)

        layout.addWidget(configs_execution_group)
        
        # BOTÕES PARA EXECUTAR/INTERROMPER
        buttons_layout = QHBoxLayout()

        self.run_btn = QPushButton("Executar")
        self.run_btn.setEnabled(False)
        play_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay) #type:ignore
        self.run_btn.setIcon(play_icon)
        buttons_layout.addWidget(self.run_btn)

        self.stop_btn = QPushButton("Parar")
        self.stop_btn.setEnabled(False)
        stop_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop) #type:ignore
        self.stop_btn.setIcon(stop_icon)
        buttons_layout.addWidget(self.stop_btn)

        layout.addLayout(buttons_layout)
        layout.addStretch()

    def validate(self):
        equation = self.input_equation.text().strip()
        x0 = self.input_xo.text().strip()

        self.current_expression = None
        self.current_x0 = None

        if(equation):
            try:
                expression = sp.sympify(equation)
                variables = expression.free_symbols

                if( 0 <  len(variables) <= 2):
                    self.current_expression = expression
                if(x0):
                    try:
                        lista_x0 = [float(valor.strip()) for valor in x0.split(",")]
                        if self.current_expression is not None and len(lista_x0) == len(variables):
                            self.current_x0 = lista_x0
                    except ValueError:
                        pass
            except Exception as e:
                pass
            
        self.equation_preview.setEnabled(self.current_expression is not None)
        self.run_btn.setEnabled(self.current_expression is not None and self.current_x0 is not None)
    
    def enable_ui(self, enable):
        self.input_equation.setEnabled(enable)
        self.equation_preview.setEnabled(enable)

        self.input_xo.setEnabled(enable)

        self.input_method.setEnabled(enable)
        self.minimum_radio.setEnabled(enable)
        self.maximum_radio.setEnabled(enable)

        self.barrier_radio.setEnabled(enable)
        self.penalty_radio.setEnabled(enable)
        self.restrictions.setEnabled(enable)

        self.input_alpha.setEnabled(enable)
        self.input_tolerance.setEnabled(enable)
        self.input_max_iterations.setEnabled(enable)

        self.hold_on.setEnabled(enable)
        self.fast_mode.setEnabled(enable)

        self.run_btn.setEnabled(enable)
        self.stop_btn.setEnabled(not enable)

    def get_data(self):
        raw_restrictions = self.restrictions.toPlainText().replace(";", "\n")
        restrictions = [restriction.strip() for restriction in raw_restrictions.split("\n") if restriction.strip()]

        return {
            "expression": self.current_expression,
            "x0": self.current_x0,
            "method": self.input_method.currentData(),
            "optimization_type": "min" if self.minimum_radio.isChecked() else "max",
            "restriction_method": "barriers" if self.barrier_radio.isChecked() else "penalty",
            "restrictions": restrictions,
            "alpha": self.input_alpha.value(),
            "tolerance": self.input_tolerance.value(),
            "max_iterations": self.input_max_iterations.value(),
            "hold_on_graph": self.hold_on.isChecked(),
            "fast_mode": self.fast_mode.isChecked()
        }