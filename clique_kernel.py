# This module provides a graph kernel based on clique counting.
import networkx as nx
import numpy as np
from tqdm import tqdm
from grakel.kernels import Kernel

from product import modular_product, relabel_product_graph
from clique_counting import count_clique_sizes

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
        clique_counts = count_clique_sizes(prod)
        return sum(clique_counts.values())
    
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
            if self._parallel is None:
                
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
            if self._parallel is None:
                for (j, y) in enumerate(Y):
                    for (i, x) in enumerate(self.X):
                        K[j, i] = self.pairwise_operation(y, x)
            return K