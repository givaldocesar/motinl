import time, traceback
import numpy as np
from utils import numpifyFunction, Camera
from methods import (Methods, create_penalized_function, create_barried_function, direcoes_aleatorias, gradiente)
from exceptions import ProcessException, StopException
from .events import EVENTS

class Process:
    def __init__(self, data=None):
        self._data = data
        self._events = {}
        self._currentPlotted = ""
        self._global_historic = {}
        self._is_running = False
    
    def on(self, event, callback):
        if(event not in self._events):
            self._events[event] = []
        
        self._events[event].append(callback)
    
    def emit(self, event, payload):
        if event in self._events:
            for callback in self._events[event]:
                callback(payload)
    
    def get_global_historic(self, method=None):
        if method is None:
            return self._global_historic
        elif method in self._global_historic:
            return self._global_historic[method]
        else:
            return None

    def set_data(self, data):
        self._data = data

    def set_running(self, is_running):
        self._is_running = is_running

    def setup(self):
        generator = None

        if(self._data):
            method = self._data["method"]
            expression_str = self._data["expression"]
            self._currentPlotted = expression_str

            if self._data["hold_on_graph"]:
                if method in self._global_historic: 
                    del self._global_historic[method]
                
                self.emit(EVENTS.DRAW_METHODS, {
                    "historic": self._global_historic,
                    "is_running": self._is_running,
                    "current_method": method
                })
              
            _, expression, var_x, var_y = numpifyFunction(expression_str)

            # Método de Restrição -----------------------------------------------------------------------------------------------------------
            if self._data["restriction_method"] == "barriers":
                weight = 15 if self._data["optimization_type"] == 'min' else -15
                penalty_f, penalty_expression = create_barried_function(expression, var_x, var_y, self._data['restrictions'], weight)
            else:
                weight = 100 if self._data["optimization_type"] == 'min' else -100
                penalty_f, penalty_expression = create_penalized_function(expression, var_x, var_y, self._data['restrictions'], weight)
            
            # Plota os gráficos da penalidade -----------------------------------------------------------------------------------------------
            self.emit(EVENTS.PLOT_GRAPHS, {
                "expression": expression_str,
                "penalty_expression": penalty_expression,
                "center": self._data['x0'],
                "radius": 10.0
            })

            # Método de otimização ---------------------------------------------------------------------------------------------------------
            if self._data["method"] == Methods.DIRECOES_ALEATORIAS:
                generator = direcoes_aleatorias(penalty_f, penalty_expression, self._data)
            elif self._data["method"] == Methods.GRADIENTE:
                generator = gradiente(penalty_f, penalty_expression, var_x, var_y, self._data)
        else:
            raise ProcessException("Não há dados para processar.")

        return generator
    
    def run(self):
        self._is_running = True
        result = (True, "")

        if self._data:
            method = self._data['method']
            expression = self._data['expression']
            
            try:
                generator = self.setup()

                if generator:
                    # MENSAGENS DE CONFIGURAÇÃO
                    print("#"*50)
                    print(f"METODO: {method.display_name}\n")
                    print(f"OTIMIZANDO A FUNCAO:\n{expression}\n")
                    print(f"X0 = ({np.round(self._data["x0"], 6)})")
                    print("RESTRICOES:")
                    for restriction in self._data['restrictions']:
                        print(f"\t## {restriction}")
                    print("\n")

                    # EXECUÇÃO DE FATO
                    current_execution = []
                    self._global_historic[method] = current_execution
                    camera = Camera(self._data['x0'], 10)
                    fast_mode = self._data["fast_mode"]
                    
                    for step_data in generator:
                        if not self._is_running:
                            raise StopException()
                        
                        current_execution.append(step_data)

                        # ignora atualização gráfica
                        if fast_mode:
                            continue

                        #move a camera para o ponto onde o algoritmo andou
                        if(camera.point_is_offscreen(step_data["x_end"])):
                            camera.set_center(step_data["x_end"])
                            self.emit("plot-graphs", {
                                "expression": expression,
                                "center": camera.center
                            })
                            
                            self.emit(EVENTS.DRAW_METHODS, {
                                "historic": self._global_historic,
                                "is_running": self._is_running,
                                "current_method": method
                            })
                        
                        self.emit(EVENTS.INSERT_TABLE_ROW, step_data["table_row"])
                        self.emit(EVENTS.STEP_EXECUTED, {
                            'method': method,
                            'data': step_data
                        })

                        time.sleep(0.05)   

                    result = (True, "Otimização concluída com sucesso.")
                else:
                    raise ProcessException(f"Método {self._data["method"]} não foi implementado.")

            except (StopException, ProcessException) as error:
                result = (False, str(error))
                print(error)
        
            except Exception as error:
                details = traceback.format_exc()
                result = (False, repr(error))
                print(details)
            finally:
                self._is_running = False
        
        return result