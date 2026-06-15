from enum import Enum

class Methods(Enum):
    DIRECOES_ALEATORIAS = (
        "Busca em Direções Aleatórias", 
        ["Iter.", "xk", "fk", "\u03B1", "dk", "status"],
        "red"
    )

    GRADIENTE = (
        "Busca pelo Gradiente",
        ["Iter.", "xk", "fk", "Gradiente", "alpha_k"],
        "cyan"
    )

    def __init__(self, display_name, headers, color):
        self.display_name = display_name
        self.headers = headers
        self.color = color

    @property
    def num_colunas(self):
        return len(self.headers)