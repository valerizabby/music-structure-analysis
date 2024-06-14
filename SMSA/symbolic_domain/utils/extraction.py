from musicaiz.loaders import Musa
import numpy as np
import networkx as nx
from musicaiz.features import (
    get_novelty_func,
    musa_to_graph
)


def feature_extraction(filename: str) -> np.array:
    musa_object = Musa(filename)
    g = musa_to_graph(musa_object)
    mat = nx.attr_matrix(g)[0]
    n = get_novelty_func(mat)
    nn = np.reshape(n, (n.size, 1))
    return nn
