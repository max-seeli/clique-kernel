# This module provides a graph kernel based on clique counting.
import networkx as nx
import numpy as np
from product import modular_product
from grakel.kernels import Kernel

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
        if type(X) == list:
            return [self.parse_input(x) for x in X]

        if not isinstance(X, nx.Graph):
            raise TypeError('Graphs must be networkx.Graph objects.')
        if len(X) == 0:
            raise ValueError('Graphs must be non-empty.')

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
        return len(list(nx.find_cliques(prod)))
        # return self.embed(x).dot(self.embed(y))
        
    
    
