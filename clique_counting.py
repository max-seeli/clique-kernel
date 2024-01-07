import networkx as nx
import numpy as np

from lightning_fast_clique_counts import get_clique_counts

def embed_graph_cliques(graph, size, approx=True):
    """
    Embed a graph into a vector of clique counts. The vector is of size
    `size`.

    Parameters
    ----------
    graph : networkx.Graph, list of networkx.Graph
        The graph to embed.
    size : int
        The size of the embedding vector to return.
    approx : bool, optional
        Whether to use the approximation algorithm. Default is None.
        When None, it is automatically determined whether to use the
        approximation algorithm based on the size of the graph.

    Returns
    -------
    embedding : numpy.ndarray
        The embedding of the graph.
    """
    if type(graph) == list:
        return np.array([embed_graph_cliques(g, size) for g in graph])

    clique_counts = count_clique_sizes(graph, approx=approx)
    return embed_clique_counts(clique_counts, size)
    

def count_clique_sizes(graph, approx=True):
    """
    Count the number of cliques of each size in a graph.

    Parameters
    ----------
    graph : networkx.Graph
        The graph to count.
    approx : bool, optional
        Whether to use the approximation algorithm. Default is None.
        When None, it is automatically determined whether to use the
        approximation algorithm based on the size of the graph.

    Returns
    -------
    clique_counts : dict
        A dictionary mapping clique size to number of cliques of that size.
    """
    if approx is None:
        approx = graph.number_of_nodes() > 50
    
    if approx:
        return get_clique_counts(graph)
    else:
        clique_counts = {}
        for clique in nx.enumerate_all_cliques(graph):
            size = len(clique)
            if size not in clique_counts:
                clique_counts[size] = 0
            clique_counts[size] += 1
        return clique_counts


def embed_clique_counts(clique_counts, size):
    """
    Embed the clique counts into a feature vector. The vector is of size
    `size`. All counts of cliques with greater size than `size` are summed
    into the 0th element of the vector. The remaining elements of the vector
    are the counts of cliques of the corresponding size.

    Parameters
    ----------
    clique_counts : dict
        A dictionary mapping clique size to number of cliques of that size.
    size : int
        The size of the feature vector to return.

    Returns
    -------
    embedding : numpy.ndarray
        The embedding of clique counts.
    """
    embedding = np.zeros(size)
    for clique_size, count in clique_counts.items():
        if clique_size > size:
            embedding[0] += count
        else:
            embedding[clique_size] += count
        
    if embedding[0] > 0:
        print("Warning: {} cliques were larger than the embedding size {}. Increase the embedding size to avoid this".format(embedding[0], size))
    return embedding