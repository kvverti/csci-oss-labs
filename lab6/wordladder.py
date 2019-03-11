"""
=====
Words
=====
Words/Ladder Graph
------------------
Generate  an undirected graph over the 5757 5-letter words in the
datafile `words_dat.txt.gz`.  Two words are connected by an edge
if they differ in one letter, resulting in 14,135 edges. This example
is described in Section 1.1 in Knuth's book (see [1]_ and [2]_).
References
----------
.. [1] Donald E. Knuth,
   "The Stanford GraphBase: A Platform for Combinatorial Computing",
   ACM Press, New York, 1993.
.. [2] http://www-cs-faculty.stanford.edu/~knuth/sgb.html
"""
# Authors: Aric Hagberg (hagberg@lanl.gov),
#          Brendt Wohlberg,
#          hughdbrown@yahoo.com

#    Copyright (C) 2004-2018 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

#    Modified by Christie Nero

import gzip
from string import ascii_lowercase as lowercase
from itertools import permutations

import networkx as nx
import sys

#-------------------------------------------------------------------
#   The Words/Ladder graph of Section 1.1
#-------------------------------------------------------------------


def generate_graph_unordered(words):
    g = nx.Graph(name="words")
    lookup = { c: lowercase.index(c) for c in lowercase }
    # return one-letter differences from each permutation.
    # strictly speaking, this only needs to deal with each
    # combination
    def edit_distance_one(word):
        # list of permutation strings
        perms = map(lambda p: ''.join(p), permutations(word))
        for perm in perms:
            for i in range(len(perm)):
                left, c, right = perm[0:i], perm[i], perm[i + 1:]
                j = lookup[c]
                for cc in lowercase[j + 1:]:
                    yield left + cc + right
    neighbors = ((word1, word2) for word1 in words
            for word2 in edit_distance_one(word1) if word2 in words)
    for w1, w2 in neighbors:
        g.add_edge(w1, w2)
    return g

def generate_graph(words):
    G = nx.Graph(name="words")
    lookup = dict((c, lowercase.index(c)) for c in lowercase)
    def edit_distance_one(word):
        for i in range(len(word)):
            left, c, right = word[0:i], word[i], word[i + 1:]
            j = lookup[c]  # lowercase.index(c)
            for cc in lowercase[j + 1:]:
                yield left + cc + right
    candgen = ((word, cand) for word in sorted(words)
               for cand in edit_distance_one(word) if cand in words)
    G.add_nodes_from(words)
    for word, cand in candgen:
        G.add_edge(word, cand)
    return G


def words_graph(file, count, gen):
    """Return the words example graph from the Stanford GraphBase"""
    fh = gzip.open(file, 'r')
    words = set()
    for line in fh.readlines():
        line = line.decode()
        if line.startswith('*'):
            continue
        w = str(line[0:count])
        words.add(w)
    return gen(words)


if __name__ == '__main__' and len(sys.argv) == 5:
    mode = sys.argv[1]
    ordered = sys.argv[2]
    src = sys.argv[3]
    dst = sys.argv[4]
    file = None
    count = None
    if mode == '5':
        file = 'words_dat.txt.gz'
        count = 5
    else:
        file = 'words4_dat.txt.gz'
        count = 4
    func = generate_graph
    if ordered == 'ordered':
        func = generate_graph
    elif ordered == 'unordered':
        func = generate_graph_unordered
    G = words_graph(file, count, func)
    print("Loaded", file)
    print("Two words are connected if they differ in one letter.")
    print("Graph has %d nodes with %d edges"
          % (nx.number_of_nodes(G), nx.number_of_edges(G)))
    print("%d connected components" % nx.number_connected_components(G))
    print("Shortest path between %s and %s is" % (src, dst))
    try:
        sp = nx.shortest_path(G, src, dst)
        for n in sp:
            print(n)
    except nx.NetworkXNoPath:
        print("None")
