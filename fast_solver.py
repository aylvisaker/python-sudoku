import time, sys, os
import itertools, random
import numpy as np
import gmpy2 as gp

# <editor-fold desc = "To do list">
# TODO try to minimize unnecessary calls to eliminate
# TODO make functions for each separate technique
# </editor-fold>

# <editor-fold desc = "Directory management and check import">
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
import sudoku, logic
def check(x)
    """
    Takes puzzle as input and returns solution provided by sudoku.py
    Both are represented by a string.
    """
    return sudoku.display(sudoku.solve(sudoku.initialize_board(x)))
# </editor-fold>

# <editor-fold desc = "Miscellaneous functions to help with readability">

n = 9

def initialize_basis(n):
    global digits = np.arange(n**2)
    global squares = np.arange(n)
    global rows = []
    global squares = set(squares)


def element_q(element, set):
    return element == element & set

def length(set)
    return gmpy2.popcount(set)

def intersect(set1, set2):
    return set1 & set2

def union(set1, set2):
    return set1 | set2

# </editor-fold>
