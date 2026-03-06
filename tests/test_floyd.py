import pytest
from floyd import floyd_warshall


def test_simple_graph():
    dist = [
        [0, 5, float('inf')],
        [5, 0, 2],
        [float('inf'), 2, 0],
    ]
    expected = [
        [0, 5, 7],
        [5, 0, 2],
        [7, 2, 0],
    ]
    d, p = floyd_warshall([row[:] for row in dist])
    assert d == expected
    # predecessor entries are not None for off-diagonal
    assert p[0][1] == 0
    assert p[0][2] == 1

    # also try with tracing enabled
    d2, p2, steps = floyd_warshall([row[:] for row in dist], trace=True)
    assert d2 == expected
    assert len(steps) == 3  # one snapshot per intermediate vertex


def test_negative_cycle():
    # graph with a negative cycle at vertex 0
    dist = [
        [0, 1],
        [float('inf'), 0],
    ]
    # add a back edge making a negative cycle
    dist[1][0] = -2
    with pytest.raises(ValueError):
        floyd_warshall([row[:] for row in dist])


def test_pred_initialization():
    # when pred is None, should create sensible matrix
    dist = [[0, 10], [10, 0]]
    d, p = floyd_warshall([row[:] for row in dist], pred=None)
    assert p[0][1] == 0
    assert p[1][0] == 1

    # check trace return structure too
    d3, p3, steps3 = floyd_warshall([row[:] for row in dist], trace=True)
    assert steps3 and isinstance(steps3, list)