# clique-kernel
A graph kernel based on clique counting of modular graphs.

## Installation

```bash
conda env create -f environment.yml
conda activate clique-kernel

git submodule update --init --recursive

python lightning_fast_clique_counts.py
```

## Modular Product of Graphs
The modular product of two graphs is a concept in graph theory that involves combining two graphs, G and H, into a single graph. This product has specific applications, particularly in subgraph isomorphism problems. The construction of the modular product graph follows this definition:

### Definition
The vertex set of the modular product is the Cartesian product of the vertex sets of the two graphs. For any two vertices $(u, v)$ and $(u', v')$ in the modular product, there is an edge between them if and only if $u$ is different from $u'$ and $v$ is different from $v'$ and either:
- **Cond. 1**: $u$ and $u'$ are adjacent in the first graph and $v$ and $v'$ are adjacent in the second graph, or
- **Cond. 2**: $u$ and $u'$ are not adjacent in the first graph and $v$ and $v'$ are not adjacent in the second graph.

$$
\text{Modular}(G, H) = (V_{\text{mod}}, E_{\text{mod}}) \\
V_{\text{mod}} = V_G \times V_H \\
E_{\text{mod}} = \{((u, v), (u', v')) \in V_{\text{mod}} \times V_{\text{mod}} \,|\, u \neq u', v \neq v', \\
((u, u') \in E_G \wedge (v, v') \in E_H) \vee ((u, u') \notin E_G \wedge (v, v') \notin E_H)\}
$$

### Application
The modular product of two graphs transforms the subgraph isomorphism problem into clique-finding problem. The construction of the modular product allows the equality of the existence of a clique with the isomorphism of the induced subgraphs (from the nodes contained in the clique) of $G$ and $H$.


## Clique Kernel
The clique kernel is a graph kernel that counts the number of cliques of size $k$ in a graph. The clique kernel is defined as follows:

$$
\text{Cliques}(G) = \{C \subseteq V_G \,|\, \forall u, v \in C, (u, v) \in E_G\} \\ 
\text{CliqueKernel}(G, H) = |\text{Cliques}(\text{Modular}(G, H))| \\
\text{CliqueKernel}_k(G, H) = |\{C \in \text{Cliques}(\text{Modular}(G, H)) \,|\, |C| = k\}|
$$

First we define the set of all cliques in the function `cliques`. Then we define two versions of the clique kernel, one that counts all cliques and one that counts cliques of size $k$.

