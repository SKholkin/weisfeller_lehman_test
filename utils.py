
import pickle

def save_instance(adj_list_1, adj_list_2, is_isomorphic, path):
    info_dict = {'adj_list_1': adj_list_1, 'adj_list_2': adj_list_2, 'is_isomorphic': is_isomorphic}
    with open(path, 'wb') as f:
        pickle.dump(info_dict, f)


def load_instance(path):
    with open(path, 'rb') as f:
        info_dict = pickle.load(f)
    adj_list_1 = []
    adj_list_2 = []
    is_isomorphic = True
    return adj_list_1, adj_list_2, is_isomorphic


def adj_matr_to_adj_list(adj_matr):
    adj_list = [[] for i in adj_matr]
    for i in range(len(adj_matr)):
        for j in range(len(adj_matr)):
            if adj_matr[i, j] == 1:
                adj_list[i].append(j)
    return adj_list
    