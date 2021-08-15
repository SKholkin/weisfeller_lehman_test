from functools import cmp_to_key


def lexicografical_compare(a: list, b: list):
    for i in range(min(len(a), len(b))):
        if a[i] > b[i]:
            return 1
        elif a[i] < b[i]:
            return -1
    if len(a) > len(b):
        return 1
    elif len(a) < len(b):
        return -1
    return 0


def wl_canonical_form(G):
    max_iter = 4
    compressed_labels = [1 for i in range(len(G))]
    neighboors_labels = [[] for i in range(len(G))]
    cur_max_label = 1
    labels = [(i, []) for i in range(len(G))]
    for iter in range(max_iter):
        for i, adj_to_i in enumerate(G):
            neighboors_labels[i] = []
            for j in adj_to_i:
                neighboors_labels[i].append(compressed_labels[j])
            neighboors_labels[i] = sorted(neighboors_labels[i])
        
        for i in range(len(G)):
            labels[i] = (i, [compressed_labels[i]] + neighboors_labels[i])
        labels = sorted(labels, key=cmp_to_key(lambda a, b: lexicografical_compare(a[1], b[1])), reverse=False)
        print(f'iter {iter} labels {labels}')

        cur_max_label += 1
        prev_part_counter = [] if iter == 0  else partitioning_counter
        partitioning_counter = [0]
        for i in range(len(labels)):
            if i > 0:
                if lexicografical_compare(labels[i][1], labels[i - 1][1]) > 0:
                    cur_max_label += 1
                    partitioning_counter.append(0)
            compressed_labels[labels[i][0]] = cur_max_label
            partitioning_counter[-1] += 1

        if partitioning_counter == prev_part_counter:
            canonical_form = sorted(compressed_labels)
            return canonical_form
        print(partitioning_counter)
        print(f'if partitioning stays the same {partitioning_counter == prev_part_counter}')
        print(f'at the end of iter {iter} compressed labels {compressed_labels}')

    print(f"WL algo didn't converged")
    return []


g = [[1, 2, 3], [0, 2], [0, 1, 4], [0, 4], [2, 3]]
wl_canonical_form(g)

def weisfeller_lehman_test(G1, G2):
    '''
    G1 and G2 are adjacency lists representing two graphs respectively
    '''
    g1_canon_form = wl_canonical_form(G1)
    g2_canon_form = wl_canonical_form(G2)
    if g1_canon_form == g2_canon_form:
        return True
    return False
