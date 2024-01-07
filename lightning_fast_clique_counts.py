"""
This module is a python wrapper for the code in the dpcolor submodule.
It is the source code of the paper "Lightning Fast and Space Efficient k-clique Counting"
by Ye et al. (https://dl.acm.org/doi/10.1145/3485447.3512167) 
"""
import networkx as nx
import os
import subprocess
from subprocess import DEVNULL

BIN_FOLDER = os.path.relpath('./dpcolor/bin/')
DATA_FOLDER = os.path.relpath('./dpcolor/data/')

def __get_programs():
    programs = {
        'makeCSR': os.path.join(BIN_FOLDER, 'makeCSR'),
        'changeToD': os.path.join(BIN_FOLDER, 'changeToD'),
        'run': os.path.join(BIN_FOLDER, 'run')
    }
    programs = {k: './' + v for k, v in programs.items()}
    return programs

def __get_paths(id):
    folder_path = os.path.join(DATA_FOLDER, f'd{id}')
    paths = {
        'folder': folder_path + os.sep,
        'data': os.path.join(folder_path, f'd{id}.txt'),
        's': os.path.join(folder_path, f's.txt'),
        'tmpedge': os.path.join(folder_path, f'tmpedge.bin'),
        'tmpidx': os.path.join(folder_path, f'tmpidx.bin'),
        'tmpedge_deg': os.path.join(folder_path, f'tmpedge.bindeg.bin'),
        'tmpidx_deg': os.path.join(folder_path, f'tmpidx.bindeg.bin'),
        'edge': os.path.join(folder_path, f'edge.bin'),
        'idx': os.path.join(folder_path, f'idx.bin')
    }
    return paths

def __create_base_files(graph, id):
    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    edgelists = nx.generate_edgelist(graph, data=False)

    paths = __get_paths(id)

    os.makedirs(paths['folder'], exist_ok=True)

    with open(paths['data'], 'w') as f:
        f.write(f'{n} {m}\n')
        f.write('\n'.join(edgelists))

    with open(paths['s'], 'w') as f:
        f.write(f'{n}')
    
    programs = __get_programs()

    subprocess.run(f'{programs["makeCSR"]} {paths["data"]} {paths["tmpedge"]} {paths["tmpidx"]}', shell=True, check=True, stdout=DEVNULL)
    subprocess.run(f'{programs["changeToD"]} -edge {paths["tmpedge"]} -idx {paths["tmpidx"]} -v {n}', shell=True, check=True, stdout=DEVNULL)
    subprocess.run(f'mv {paths["tmpedge_deg"]} {paths["edge"]}', shell=True, check=True)
    subprocess.run(f'mv {paths["tmpidx_deg"]} {paths["idx"]}', shell=True, check=True)


def __cleanup(id):
    paths = __get_paths(id)
    subprocess.run(f'rm -rf {paths["folder"]}', shell=True, check=True)


def __dpcolor_path(id, k, N):

    # ./bin/run -f {folder} -k {k} -N {N} -cccpath
    # read the output of the command from stdout
    output = subprocess.check_output(f'{__get_programs()["run"]} -f {__get_paths(id)["folder"]} -k {k} -N {N} -cccpath', shell=True, text=True)

    # parse the output of structure:
    # '|9| 1.0| 1000| 0.02| 300| d8| 258.0|not expected 6 | 0.000000 0 1000 -inf%| 258| 100.00%| 0.05| 0.07| inf%'
    # return number after the 7th pipe (after d...)
    split = output.split('|')
    return int(float(split[7].strip()))

def __get_k_clique_count(id, k):
    # run dpcolor
    return __dpcolor_path(id, k, 1000)

def get_clique_counts(graph, id="graph"):

    # Create base files
    __create_base_files(graph, id)

    n = graph.number_of_nodes()

    clique_counts = {}
    for k in range(3, n+1):
        clique_counts[k] = __get_k_clique_count(id, k)
        if clique_counts[k] == 0:
            break
    
    __cleanup(id)
    return clique_counts

def get_k_clique_count(graph, k, id="graph"):

    # Create base files
    __create_base_files(graph, id)

    count = __get_k_clique_count(id, k)
    __cleanup(id)
    return count


if __name__ == '__main__':

    # Initialize the dpcolor submodule
    os.makedirs(BIN_FOLDER, exist_ok=True)

    # Compile the dpcolor submodule
    subprocess.run('make bin/run', shell=True, check=True, cwd='./dpcolor')
    subprocess.run('make bin/changeToD', shell=True, check=True, cwd='./dpcolor')
    subprocess.run('make bin/makeCSR', shell=True, check=True, cwd='./dpcolor')

