# This module provides a graph kernel based on clique counting.
import networkx as nx
import numpy as np
from product import modular_product, relabel_product_graph
from grakel.kernels import Kernel
from lightning_fast_clique_counts import get_clique_counts

class CliqueKernel(Kernel):

    def __init__(self, normalize=True, verbose=False):
        """
        Parameters
        ----------
        size : int
            The size of the clique to count.
        normalize : bool
            Whether to normalize the kernel matrix.
        verbose : bool
            Whether to print progress information.
        """
        super().__init__(verbose=verbose)
        self.normalize = normalize

    def parse_input(self, X):
        """
        Parse and check the given input for the kernel.

        Parameters
        ----------
        X : list of networkx.Graph
            The list of graphs to compute the kernel matrix for.

        Returns
        -------
        X : list of networkx.Graph
            The list of graphs to compute the kernel matrix for.
        """
        if type(X) != list:
            raise TypeError('Input must be a list of networkx.Graph objects.')
        
        for i, x in enumerate(X):

            if not isinstance(x, nx.Graph):
                raise TypeError('Graphs must be networkx.Graph objects.')
            if len(x) == 0:
                raise ValueError('Graphs must be non-empty.')

            x.graph['id'] = str(i)

        return X
    
    def pairwise_operation(self, x, y):
        """
        Calculate a pairwise kernel between two elements.

        Parameters
        ----------
        x, y : networkx.Graph
            The two elements to compute the kernel for.
        
        Returns
        -------
        kernel : number
            The kernel value.
        """
        prod = modular_product(x, y)
        prod = relabel_product_graph(prod)
        mod_id = x.graph['id'] + '_' + y.graph['id']
        clique_counts = get_clique_counts(prod, mod_id)
        return sum(clique_counts.values())
        # return self.embed(x).dot(self.embed(y))
        
    
    
