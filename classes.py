"""
15-251 Great Ideas in Theoretical Computer Science
Assignment: Reductions
Version: Spring 2025

Utility file defining useful Python classes
"""
from typing import List

class UGraph:
    """
    For simplicity, let V = [n] = {1, 2, ..., n}. 
    Parameters:
        - n: number of vertices
        - E: list of edges of form [u, v] (list of integers of length 2)

    ex) n = 3, E = [[1, 2], [2, 3], [1, 3]] (triangle graph)
    ex) n = 5, E = [[1, 2], [1, 3], [1, 4], [1, 5]] (star graph with vertex 1 as the center)

    Note: the Python class will also generate the adjacency list corresponding to the edge set.
    i.e. you can access the neighbors of vertex u via A[u] = list of u's neighbors
    """
    def __init__(self, n, E):
        self.n = n # number of vertices
        self.E = E # edge set
        self.validate()
        self.A = {a : [] for a in range(1, n+1)} # Adjacency list
        for edge in E:
            u, v = edge[0], edge[1]
            self.A[u].append(v)
            self.A[v].append(u)

    def validate(self):
        try:
            for edge in self.E:
                if len(edge) != 2: raise InvalidUGraph
                if (edge[0] < 1 or edge[0] > self.n): raise InvalidUGraph
                if (edge[1] < 1 or edge[1] > self.n): raise InvalidUGraph
        except:
            raise InvalidUGraph

    def __repr__(self):
        return str({'n': self.n, 'E': self.E})
    

class InvalidUGraph(Exception):
    pass


class CNF:
    """ 
    k-CNF is represented as a List of List of int 
    Parameters:
        - formula: boolean formula of format List of List of int
            ex) [[1, -2, 3], [4, 1, -2], ...] represents (x1 or not x2 or x3) and (x4 or x1 or not x2), etc
        - k: specify number of literals in each clause. For generic CNF, let k be None
    """
    def __init__(self, formula, k=None) -> None:
        self.formula = formula
        self.k = k
        self.validate()

    def validate(self):
        if self.k is None: return
        try:
            for clause in self.formula:
                if len(clause) != self.k: raise InvalidCNF(self.k)
        except:
            raise InvalidCNF(self.k)

    def __repr__(self):
        return str(self.formula)


class InvalidCNF(Exception):
    def __init__(self, k):
        super().__init__(f"Invalid {k}CNF")


class Matrix:
    """
    Matrix of size n x m.
    Parameters
        - M: List of List of int
            ex) [[1, 2, 3], [4, 5, 6]] is a 2 x 3 matrix
    """
    def __init__(self, M: List[List[int]]) -> None:
        self.M = M
        self.validate()

    def validate(self):
        try:
            n = len(self.M)
            m = len(self.M[0])
            for i in range(n):
                if len(self.M[i]) != m:
                    raise InvalidMatrix
        except:
            raise InvalidMatrix


class DistanceMatrix(Matrix):
    """
    DistanceMatrix is a symmetric square matrix
    """
    def __init__(self, M) -> None:
        super().__init__(M)

    def validate(self):
        super().validate()
        n = len(self.M)
        m = len(self.M[0])
        if n != m: # must be square matrix
            raise InvalidDistanceMatrix
        self.n = n
        
        # We want D[i][j] = D[j][i]
        for i in range(n):
            for j in range(i+1, n):
                if self.M[i][j] != self.M[j][i]:
                    raise InvalidDistanceMatrix


class ZPMOMatrix(Matrix):
    """
    ZPMOMatrix is a matrix with all elements 0, +1, -1.
    """
    def __init__(self, M) -> None:
        super().__init__(M)
        
    def validate(self):
        super().validate()
        self.n = len(self.M)
        self.m = len(self.M[0])

        # All entries should be 0, +1, -1
        for i in range(self.n):
            for j in range(self.m):
                if self.M[i][j] not in [-1, 0, 1]:
                    raise InvalidZPMOMatrix


class InvalidMatrix(Exception):
    pass

class InvalidDistanceMatrix(InvalidMatrix):
    pass

class InvalidZPMOMatrix(InvalidMatrix):
    pass


# Examples
phi = CNF(formula=[[1, 2, 3], [1, 4, 5]], k=3)
G = UGraph(n=3, E=[[1, 2], [2, 3]])
M = Matrix([[0, 1], [1, 2], [2, 3]])
M = DistanceMatrix([[0, 1], [1, 2]])
M = ZPMOMatrix([[0, 1], [0, -1]])
