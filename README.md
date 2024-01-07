# clique-kernel
A graph kernel based on clique counting of modular graphs.

## Installation

```bash
conda env create -f environment.yml
conda activate clique-kernel

git submodule update --init --recursive

python lightning_fast_clique_counts.py
```