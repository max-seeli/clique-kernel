import networkx as nx
from itertools import product

def modular_product(G, H):
    """
    Get the modular product of two graphs.

    Definition
    ----------
    The vertex set of the modular product is the Cartesian product of the 
    vertex sets of the two graphs. For any two vertices `(u, v)` and `(u', v')`
    in the modular product, there is an edge between them if and only if
    `u` is different from `u'` and `v` is different from `v'` and either:
    - `u` and `u'` are adjacent in the first graph and `v` and `v'` are adjacent
        in the second graph, or
    - `u` and `u'` are not adjacent in the first graph and `v` and `v'` are not
        adjacent in the second graph.

    Parameters
    ----------
    G : networkx.Graph
        The first graph.
    H : networkx.Graph
        The second graph.

    Returns
    -------
    M : networkx.Graph
        The modular product of G and H.
    """
    M = nx.Graph()

    # Cartesian product of the vertex sets
    for (u, v) in product(G.nodes(), H.nodes()):
        M.add_node((u, v))

    # Add edges based on the conditions
    for (u, v) in M.nodes():
        for (u_prime, v_prime) in M.nodes():
            if u != u_prime and v != v_prime:
                condition1 = G.has_edge(u, u_prime) and H.has_edge(v, v_prime)
                condition2 = not G.has_edge(u, u_prime) and not H.has_edge(v, v_prime)
                if condition1 or condition2:
                    M.add_edge((u, v), (u_prime, v_prime))
    return M


def relabel_product_graph(graph):
    """
    Relabel the nodes of a product graph. The nodes are labeld with integers,
    avoiding the use of tuples as node labels. 

    Parameters
    ----------
    graph : networkx.Graph
        The graph to relabel.

    Returns
    -------
    graph : networkx.Graph
        The relabeled graph.
    """
    mapping = {}
    for i, node in enumerate(graph.nodes()):
        mapping[node] = i
    return nx.relabel_nodes(graph, mapping)