class ProcessException(Exception):
    def __init__(self, message):
        super().__init__(f"ERRO DE PROCESSAMENTO: {message}")