import numpy as np
from utils import evaluate_f

def direcoes_aleatorias(func, expr, data):
    """
        Executa o método das Direções Aleatórias.
        
        Parâmetros:
        func: Função NumPy gerada pelo lambdify.
        data: Dicionário com as seguintes chaves =>
            -x0: Lista ou array com o ponto inicial [x, y].
            -alpha_inicial: Tamanho do passo inicial.
            -tolerance: Tolerância (critério de parada para o passo).
            -max_iterations: Número máximo de iterações permitidas.
        
        Retorna:
        ponto_minimo (array), historico (lista de dicionários para a tabela)
    """
    x_atual = np.array(data["x0"], dtype=float)
    f_atual = evaluate_f(func, x_atual)
    alpha = data["alpha"]
    max_iterations = data["max_iterations"]
    tolerance = data["tolerance"]
    optimization_type = data['optimization_type']
    
    iteration = 1
    trial = 1
    falhas_consecutivas = 0
    MAX_FALHAS = 5

    while (max_iterations == 0 or iteration <= max_iterations) and alpha > tolerance:
        if(iteration > max(10000, max_iterations)):
            break

        # 1. Gera um vetor aleatório do mesmo tamanho de X (ex: 2D)
        u = np.random.randn(len(x_atual))
        
        # 2. Normaliza para virar um vetor de comprimento 1 (direção pura)
        direction = u / np.linalg.norm(u)
        
        #Guarda os valores para desenhar o gráfico
        x_start = x_atual.copy()
        f_start = f_atual

        # 3. Dá o passo e cria o ponto candidato
        x_candidato = x_atual + (alpha * direction)
        f_candidato = evaluate_f(func, x_candidato)
        
        # Prepara os dados para a tabela
        if(len(x_atual) > 1):
            str_xk = f"[{x_atual[0]:.8f}, {x_atual[1]:.8f}]"
            str_direction = f"[{direction[0]:.8f}, {direction[1]:.8f}]"
        else:
            str_xk = f"[{x_atual[0]:.8f}]"
            str_direction = f"[{direction[0]:.8f}]"
        
        text_iteration = f"{iteration} (Tent. {trial})"
        
        # 4. Avalia se o passo foi bom ou ruim
        status = "Rejeitado"
        if (optimization_type == 'max' and f_candidato > f_atual) or (optimization_type == 'min' and f_candidato < f_atual):
            status = 'Aceito'
        
        
        if status == 'Aceito':
            # Salva o estado atual ANTES de atualizar
            table_row = [text_iteration, str_xk, f"{f_atual:.8f}",f"{alpha:.8f}", str_direction, status]
            
            # Atualiza a posição
            x_atual = x_candidato
            f_atual = f_candidato
            iteration += 1
            trial = 1
            falhas_consecutivas = 0 # Reseta o contador de falhas
            
        else:
            table_row = [text_iteration, str_xk, f"{f_atual:.8f}", f"{alpha:.8f}", str_direction, status]
            
            falhas_consecutivas += 1
            trial += 1
            
            # Se bateu muito a cabeça na parede, diminui o passo
            if falhas_consecutivas >= MAX_FALHAS:
                alpha = alpha / 2.0
                falhas_consecutivas = 0
        
        yield {
            "table_row": table_row,
            "x_start": x_start,
            "x_end": x_candidato,
            "z_start": f_start,
            "z_end": f_candidato,
            "status": status,
            "x_final": x_atual,
            "z_final": f_atual
        }