# This module provides a graph kernel based on clique counting.
import networkx as nx
import numpy as np
from tqdm import tqdm
from grakel.kernels import Kernel

from product import modular_product, relabel_product_graph
from clique_counting import count_clique_sizes, count_k_cliques

class CliqueKernel(Kernel):

    def __init__(self, k, approx=True, normalize=True, verbose=False):
        """
        Parameters
        ----------
        k : int
            The size of the cliques to count. Must be at least 2 or None.
            If None, the kernel is calculated for all clique sizes.
        approx : bool, optional
            Whether to use the approximation algorithm. Default is True.
            If None, it is automatically determined whether to use the
            approximation algorithm based on the size of the graph.
        normalize : bool, optional
            Whether to normalize the kernel matrix.
        verbose : bool, optional
            Whether to print progress information.
        """
        super().__init__(normalize=normalize, verbose=verbose)
        self.k = k
        self.approx = approx
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
        if self.k is None:
            clique_counts = count_clique_sizes(prod, approx=self.approx)
            return sum(clique_counts.values())
        else:
            return count_k_cliques(prod, self.k, approx=self.approx)
    
    def _calculate_kernel_matrix(self, Y=None):
        """Calculate the kernel matrix given a target_graph and a kernel.

        Each a matrix is calculated between all elements of Y on the rows and
        all elements of X on the columns.

        Parameters
        ----------
        Y : list, default=None
            A list of graph type objects. If None kernel is calculated between
            X and itself.

        Returns
        -------
        K : numpy array, shape = [n_targets, n_inputs]
            The kernel matrix: a calculation between all pairs of graphs
            between targets and inputs. If Y is None targets and inputs
            are the taken from self.X. Otherwise Y corresponds to targets
            and self.X to inputs.

        Notes
        -----
        This funcition is based on the implementation of the base class,
        but it is modified to use a progress bar.
        """
        if Y is None:
            K = np.zeros(shape=(len(self.X), len(self.X)))
                
            n = len(self.X)
            total_operations = n * (n + 1) // 2  # Total number of operations
            progress_bar = tqdm(total=total_operations, desc="Processing")

            cache = list()
            for (i, x) in enumerate(self.X):
                K[i, i] = self.pairwise_operation(x, x)
                progress_bar.update(1)
                for (j, y) in enumerate(cache):
                    K[j, i] = self.pairwise_operation(y, x)
                    progress_bar.update(1)
                cache.append(x)
            progress_bar.close()
            K = np.triu(K) + np.triu(K, 1).T

        else:
            K = np.zeros(shape=(len(Y), len(self.X)))
            
            total_operations = len(Y) * len(self.X)
            progress_bar = tqdm(total=total_operations, desc="Processing")

            for (j, y) in enumerate(Y):
                for (i, x) in enumerate(self.X):
                    K[j, i] = self.pairwise_operation(y, x)
                    progress_bar.update(1)
        return K