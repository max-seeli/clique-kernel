# Full code combining all steps
from grakel import GraphKernel
import networkx as nx
from clique_kernel import CliqueKernel
from grakel.datasets import fetch_dataset
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score

import random

# Load dataset
MUTAG = fetch_dataset("MUTAG", verbose=False)
G, y = MUTAG.data, MUTAG.target
print(len(G))

print(G[0][0])
G = [(g[0], g[1]) for g in G]

# Transform graphs to networkx.Graph objects
# for each graph g[0] is the adjacency matrix and g[1] are the node labels
G = [nx.from_edgelist(g[0]) for g in G]
print(G[0].edges())


G_train, G_test, y_train, y_test = train_test_split(G, y, test_size=0.2)
print("Number of graphs (train/test): {}/{}".format(len(G_train), len(G_test)))

# Print graph from training set with maximum number of nodes
max_nodes = max([len(g) for g in G_train])
print(max_nodes)

# Define the kernel
kernel = CliqueKernel(normalize=True, verbose=True)

# Compute the kernel matrix
print("Computing the kernel matrix...", end="", flush=True)
K = kernel.fit_transform(G_train)
print("done")

# Train the classifier
clf = SVC()

# 10-fold cross validation
print("Validating...", end="", flush=True)
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Randomized search for hyperparameter optimization
param_grid = {"C": [2**i for i in range(-5, 15, 2)], 
              "gamma": [2**i for i in range(-15, 3, 2)]}
search = RandomizedSearchCV(clf, param_grid, cv=cv, n_iter=50, verbose=1)
search.fit(K, y_train)
print("done")

# Evaluate the model
print("Testing...", end="", flush=True)
K_test = kernel.transform(G_test)
y_pred = search.predict(K_test)
print("done")

print("Accuracy score: {}".format(accuracy_score(y_test, y_pred)))

