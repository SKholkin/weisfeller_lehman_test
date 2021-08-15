import argparse
from copy import deepcopy
from math import radians
import random
import os.path as osp
from argparse import ArgumentParser

import numpy as np
from numpy.lib.function_base import copy

from utils import save_instance, adj_matr_to_adj_list


def basic_graph_gen(n, p):
    # Erdős–Rényi <G,p> model
    adj_matr = np.random.choice([0, 1], size=[n, n], p=[1 - p, p])
    # make the matrix symmetric
    lower_ind = np.tril_indices(n, -1)
    adj_matr[lower_ind] = adj_matr.T[lower_ind]
    np.fill_diagonal(adj_matr, 0)
    return adj_matr


def gen_adversarial_instance(adj_matr):
    raise NotImplementedError('Too weak algorihm to generate non isomorphic graphs. Waiting for better algorithm.')
    # add an edge
    adj_matr = deepcopy(adj_matr)
    not_edges = []
    edges = []
    for i in range(len(adj_matr)):
        for j in range(len(adj_matr)):
            if i != j:
                if adj_matr[i, j] == 0:
                    not_edges.append((i, j))
                else:
                    edges.append((i, j))

    if len(not_edges) == 0 or len(edges) == 0:
        return None
    edge_to_add = np.random.randint(len(not_edges))
    edge_to_del = np.random.randint(len(edges))
    adj_matr[not_edges[edge_to_add][0], not_edges[edge_to_add][1]] = 1
    adj_matr[not_edges[edge_to_add][1], not_edges[edge_to_add][0]] = 1
    print(f'add edge {not_edges[edge_to_add][0]}:{not_edges[edge_to_add][1]}')
    adj_matr[edges[edge_to_del][0], edges[edge_to_del][1]] = 0
    adj_matr[edges[edge_to_del][1], edges[edge_to_del][0]] = 0
    print(f'del edge {edges[edge_to_del][0]}:{edges[edge_to_del][1]}')
    return adj_matr


def permute_graph(adj_matr):
    # create a permutation
    permutation = [i for i in range(len(adj_matr))]
    random.shuffle(permutation)
    permuted_adj = np.zeros_like(adj_matr)
    for i_perm, i in enumerate(permutation):
        for j_perm, j in enumerate(permutation):
            permuted_adj[i_perm, j_perm] = adj_matr[i, j]
    return permuted_adj


def create_dataset(samples, path, n_min, n_max, p=0.5):
    for iter in range(samples):
        if iter // (samples // 10 if samples > 10 else 1):
            print(f'{iter - 1} samples generated')
        # random choose n vertices
        n_vertices = random.randint(n_min, n_max)
        # create first graph
        graph_1 = basic_graph_gen(n_vertices, p)
        # if random choose to be adversarial p = 0.5 : create adv_graph
        is_isomorphic = True
        if random.randint(0, 1) == 1:
            graph_2 = gen_adversarial_instance(graph_1)
            if graph_2 is None:
                # fully connected or empty graphs don't make any sense
                continue
            is_isomorphic = False
        else:
            graph_2 = deepcopy(graph_1)
        # permute second graph
        graph_2 = permute_graph(graph_2)
        # gen both adj lists
        graph_1_adj_list = adj_matr_to_adj_list(graph_1)
        graph_2_adj_list = adj_matr_to_adj_list(graph_2)
        print(f'graph 1 {graph_1_adj_list}\ngraph 2 {graph_2_adj_list} is isomorphic {is_isomorphic}')
        # save graphs as a pair
        instance_path = osp.join(path, f'{iter}.inst')
        save_instance(graph_1_adj_list, graph_2_adj_list, is_isomorphic, instance_path)


if __name__  == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--samples', type=int, help='Number of samples for dataset')
    parser.add_argument('--path', type=str, help='Path to save dataset')
    parser.add_argument('--nmin', type=int, help='Minimal number of vertices in dataset', default=10)
    parser.add_argument('--nmax', type=int, help='Maximum number of vertices in dataset', default=20)
    parser.add_argument('--graph_density', type=float, help='Mean density of graphs', default=0.5)
    args = parser.parse_args()
    create_dataset(args.samples, args.path, args.nmin, args.nmax, args.graph_density)
