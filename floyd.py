def floyd_warshall(dist, pred=None, trace=False):
    import copy

    n = len(dist)
    
    # Garantir que a matriz é quadrada
    for row in dist:
        if len(row) != n:
            raise ValueError("A matriz de distâncias deve ser quadrada.")

    # Inicialização da matriz de predecessores se não fornecida
    if pred is None:
        pred = [[i if (i != j and dist[i][j] != float('inf')) else None 
                 for j in range(n)] for i in range(n)]

    steps = []
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # Melhoria na lógica de soma com infinito
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[k][j]
        
        if trace:
            steps.append(copy.deepcopy(dist))

    # Deteção de ciclos negativos
    for i in range(n):
        if dist[i][i] < 0:
            raise ValueError("Ciclo negativo detetado no vértice {}".format(i))

    if trace:
        return dist, pred, steps
    return dist, pred