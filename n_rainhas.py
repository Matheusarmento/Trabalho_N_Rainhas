
import heapq
import time

# Calcula a quantidade de pares de rainhas em conflito
def calcular_heuristica(estado):
    conflitos = 0

    for linha1 in range(len(estado)):
        for linha2 in range(linha1 + 1, len(estado)):
            coluna1 = estado[linha1]
            coluna2 = estado[linha2]

            mesma_coluna = coluna1 == coluna2
            mesma_diagonal = abs(coluna1 - coluna2) == abs(linha1 - linha2)

            if mesma_coluna or mesma_diagonal:
                conflitos += 1

    return conflitos


# Calcula os conflitos criados pela nova rainha
def conflitos_nova_rainha(estado, coluna):
    nova_linha = len(estado)
    conflitos = 0

    for linha, outra_coluna in enumerate(estado):
        if outra_coluna == coluna:
            conflitos += 1
        elif abs(outra_coluna - coluna) == abs(linha - nova_linha):
            conflitos += 1

    return conflitos


# Gera novos estados adicionando uma rainha na próxima linha
def gerar_sucessores(estado, heuristica_atual, n):
    for coluna in range(n):
        novo_estado = estado + (coluna,)

        nova_heuristica = (
            heuristica_atual
            + conflitos_nova_rainha(estado, coluna)
        )

        yield novo_estado, nova_heuristica


# Algoritmo A*
def busca_a_estrela(n, limite_expansoes, limite_gerados):
    inicio = time.perf_counter()

    fila = [(0, 0, 0, ())]
    visitados = {()}

    expandidos = 0
    gerados = 0

    while fila and expandidos < limite_expansoes and gerados < limite_gerados:

        _, h, custo, estado = heapq.heappop(fila)
        expandidos += 1

        if len(estado) == n and h == 0:
            tempo = time.perf_counter() - inicio
            return estado, expandidos, gerados, tempo, "Solução encontrada"

        for novo_estado, nova_h in gerar_sucessores(estado, h, n):

            if novo_estado not in visitados:
                visitados.add(novo_estado)
                gerados += 1

                novo_custo = custo + 1
                f = novo_custo + nova_h

                heapq.heappush(
                    fila,
                    (f, nova_h, novo_custo, novo_estado)
                )

                if gerados >= limite_gerados:
                    break

    tempo = time.perf_counter() - inicio

    if not fila:
        status = "Busca encerrada sem solução"
    else:
        status = "Limite de busca atingido"

    return None, expandidos, gerados, tempo, status


# Algoritmo de Busca Gulosa
def busca_gulosa(n, limite_expansoes, limite_gerados):
    inicio = time.perf_counter()

    fila = [(0, 0, ())]
    visitados = {()}

    expandidos = 0
    gerados = 0

    while fila and expandidos < limite_expansoes and gerados < limite_gerados:

        h, profundidade_negativa, estado = heapq.heappop(fila)
        expandidos += 1

        if len(estado) == n and h == 0:
            tempo = time.perf_counter() - inicio
            return estado, expandidos, gerados, tempo, "Solução encontrada"

        for novo_estado, nova_h in gerar_sucessores(estado, h, n):

            if novo_estado not in visitados:
                visitados.add(novo_estado)
                gerados += 1

                heapq.heappush(
                    fila,
                    (nova_h, -(len(novo_estado)), novo_estado)
                )

                if gerados >= limite_gerados:
                    break

    tempo = time.perf_counter() - inicio

    if not fila:
        status = "Busca encerrada sem solução"
    else:
        status = "Limite de busca atingido"

    return None, expandidos, gerados, tempo, status


# Exibe o tabuleiro encontrado
def mostrar_tabuleiro(solucao):
    if solucao is None:
        return

    n = len(solucao)

    if n > 20:
        print("Tabuleiro ocultado para evitar muitas linhas.")
        return

    print("\nTabuleiro encontrado:")

    for coluna_rainha in solucao:
        linha = ["."] * n
        linha[coluna_rainha] = "Q"
        print(" ".join(linha))


# Executa os algoritmos
def executar(n):

    limite_expansoes = min(50000, max(500, 200000 // n))
    limite_gerados = 200000

    print(f"\nPROBLEMA DAS {n} RAINHAS")
    print(f"Limite de expansões: {limite_expansoes}")
    print(f"Limite de estados gerados: {limite_gerados}")

    algoritmos = [
        ("A*", busca_a_estrela),
        ("Busca Gulosa", busca_gulosa)
    ]

    for nome, algoritmo in algoritmos:

        solucao, passos, gerados, tempo, status = algoritmo(
            n, limite_expansoes, limite_gerados
        )

        print(f"\n{nome}")
        print(f"Status: {status}")
        print(f"Estados expandidos: {passos}")
        print(f"Estados gerados: {gerados}")
        print(f"Tempo: {tempo:.6f} segundos")

        if solucao is not None:
            print("Heurística final:", calcular_heuristica(solucao))
            mostrar_tabuleiro(solucao)


# Programa principal
if __name__ == "__main__":

    try:
        quantidade = int(input("Digite a quantidade de rainhas: "))

        if quantidade < 1:
            print("Digite um número maior que zero.")
        else:
            executar(quantidade)

    except ValueError:
        print("Entrada inválida. Digite um número inteiro.")