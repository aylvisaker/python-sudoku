import time
import random

specials = '0.'
digits = '123456789'
blocks = ['123', '456', '789']


def cross(A,B):
    return [a + b for a in A for b in B]

squares = cross(digits, digits)
therows = [cross(x,digits) for x in digits]
thecolumns = [cross(digits, x) for x in digits]
theboxes = [cross(x,y) for x in blocks for y in blocks]
thegroups = therows + thecolumns + theboxes

neighborhoods = dict((s, [g for g in thegroups if s in g]) for s in squares)
neighbors = dict((s, set([i for nbhd in neighborhoods[s] for i in nbhd]) - {s}) for s in squares)


def initialize_board(v):
    b = {s: digits for s in squares}
    for i, s in enumerate(squares):
        if v[i] not in specials:
            fillin(b, s, v[i])
    return b


def fillin(b, s, n):
    leftover = b[s].replace(n, '')
    if all(eliminate(b, s, x) for x in leftover):
        return b
    else:
        return False


def eliminate(b, s, n):
    if not(n in b[s]):
        return b
    b[s] = b[s].replace(n, '')
    if len(b[s]) == 0:
        return False
    elif len(b[s]) == 1:
        if not all(eliminate(b, r, b[s]) for r in neighbors[s]):
            return False
    return b


def solve(b):
    if b is False:
        return False
    if all(len(b[s]) == 1 for s in squares):
        return b
    i, s = min((len(b[s]), s) for s in squares if len(b[s]) > 1)
    candidates = ''.join(random.sample(b[s], len(b[s])))
    for cand in candidates:
        d = b.copy()
        d = fillin(d, s, cand)
        d = solve(d)
        if d:
            return d


def display(b):
    if b is False:
        return False
    line = ''.join(b[s] for s in squares)
    return(line)

v = '........1.......2......3.......4.5....6...3....781.....1..2...4.3.....7.95.......'
board = solve(initialize_board(v))
print(v)
print(display(board))