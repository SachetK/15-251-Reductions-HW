"""
15-251 Great Ideas in Theoretical Computer Science
Assignment: Reductions
Version: Spring 2025

STARTER CODE
"""
from classes import UGraph, CNF, DistanceMatrix, ZPMOMatrix
from typing import Tuple, List


""" 
Show that EQUAL-COL is NP-hard.
- Input: x is an object representing the instance you are reducing from
- Output: a UGraph object representing a EQUAL-COL instance
"""
choice_EQUAL_COL_reduce_from = "3COL"

def to_EQUAL_COL(G) -> UGraph:
    E = []
    # Step 1: within-triple triangles
    for v in range(1, G.n + 1):
        v1, v2, v3 = 3 * (v - 1) + 1, 3 * (v - 1) + 2, 3 * (v - 1) + 3
        E += [[v1, v2], [v2, v3], [v3, v1]]

    # Step 2: connect corresponding copies
    for (u, v) in G.E:
        for i in range(3):
            E.append([3 * (u - 1) + i + 1, 3 * (v - 1) + i + 1])

    # Step 3: add anchor triangle
    t1, t2, t3 = 3 * G.n + 1, 3 * G.n + 2, 3 * G.n + 3
    E += [[t1, t2], [t2, t3], [t3, t1]]

    # Step 4: connect each column to its anchor
    for v in range(1, G.n + 1):
        v1, v2, v3 = 3 * (v - 1) + 1, 3 * (v - 1) + 2, 3 * (v - 1) + 3
        E += [[v1, t1], [v2, t2], [v3, t3]]

    return UGraph(3 * G.n + 3, E)

"""
The type of UNITED-NATIONS is a tuple (k, D, t, n):
- k (int): number of countries. Assume countries are labeled by 0, 1, 2, ..., k-1
- D (DistanceMatrix): D[i][j] is the distance between countries c_i and c_j
- t (int)
- n (int)

Show that UNITED-NATIONS is NP-hard.
Input: x is an object representing the instance you are reducing from
Output: a tuple (k, D, t, n) representing a UNITED-NATIONS instance
"""
choice_UNITED_NATIONS_reduce_from = "3COL"
def to_UNITED_NATIONS(G) -> Tuple[int, DistanceMatrix, int, int]:

    k = G.n
    M = [[2 for _ in range(k)] for _ in range(k)]

    for i in range(k):
        M[i][i] = 1

    # edges get distance 1, adjust 1-based to 0-based
    for (u, v) in G.E:
        u0 = u - 1
        v0 = v - 1
        M[u0][v0] = 1
        M[v0][u0] = 1  # symmetry

    # wrap in DistanceMatrix
    D = DistanceMatrix(M)
    t = 1
    n = 3

    return k, D, t, n


"""
Show that NONZERO-MATRIX is NP-hard.
Input: x is an object representing the instance you are reducing from
Output: a ZPMOMatrix object M representing a NONZERO-MATRIX instance
"""
choice_NONZERO_MATRIX_reduce_from = "3SAT"
def to_NONZERO_MATRIX(C) -> ZPMOMatrix:
    if C.k != 3:
        return ZPMOMatrix([[0]])

    # Step 1: collect distinct variables
    variables = sorted({abs(lit) for clause in C for lit in clause})
    num_vars = len(variables)
    num_clauses = len(C)

    # mapping: variable -> row index
    var_to_index = {v: i for i, v in enumerate(variables)}

    # Step 2: initialize matrix
    M = [[0 for _ in range(num_clauses)] for _ in range(num_vars)]

    # Step 3: fill matrix
    for j, clause in enumerate(C):  # column = clause index
        for lit in clause:
            row = var_to_index[abs(lit)]
            if lit > 0:
                M[row][j] = 1
            else:
                M[row][j] = -1

    return ZPMOMatrix(M)


# DO NOT EDIT
choices = {
    "EQUAL-COL": choice_EQUAL_COL_reduce_from,
    "UNITED-NATIONS": choice_UNITED_NATIONS_reduce_from, 
    "NONZERO-MATRIX": choice_NONZERO_MATRIX_reduce_from 
}
