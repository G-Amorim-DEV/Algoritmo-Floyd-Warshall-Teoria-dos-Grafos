def floyd_warshall(dist, pred=None, trace=False):
    """Run the Floyd–Warshall algorithm on a distance matrix.

    Parameters
    ----------
    dist : list of list of numbers
        Square matrix of edge weights; use a large number (e.g. 9999 or
        float('inf')) to represent no direct edge between vertices.
    pred : list of list of int or None, optional
        Predecessor matrix; ``pred[i][j]`` should be the index of the vertex
        immediately preceding ``j`` on the shortest path from ``i``. If
        ``None`` a default matrix is created with ``pred[i][j] = i`` for
        ``i != j`` and ``None`` on the diagonal.
    trace : bool, optional
        If ``True`` the function collects and returns a list of snapshots
        showing the distance matrix after each intermediate vertex ``k`` is
        processed. This can be used for debugging or educational purposes.

    Returns
    -------
    If ``trace`` is ``False`` (the default) returns
    ``(dist, pred)``. If ``trace`` is ``True`` returns ``(dist, pred, steps)``
    where ``steps`` is a list of distance matrices (each a deep copy) after
    each iteration of ``k``.

    Raises
    ------
    ValueError
        If a negative cycle is detected (i.e. distance from a vertex to
        itself becomes negative).
    """
    import copy

    n = len(dist)

    # lazy initialize predecessor matrix if not provided
    if pred is None:
        pred = [[i if i != j else None for j in range(n)] for i in range(n)]

    steps = []
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]
        if trace:
            steps.append(copy.deepcopy(dist))

    # check for negative cycles
    for i in range(n):
        if dist[i][i] < 0:
            raise ValueError("negative cycle detected")

    if trace:
        return dist, pred, steps
    return dist, pred