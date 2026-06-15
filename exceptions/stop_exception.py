class StopException(Exception):
    def __init__(self):
        super().__init__("Otimização encerrada pelo Usuário")