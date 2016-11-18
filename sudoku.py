import time
import random
import sys

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


def main():
    if len(sys.argv) > 1:
        file = open(sys.argv[1], 'r')
    else: file = open('boards0.txt', 'r')
    puzzles = file.readlines()
    puzzles = [p[:81] for p in puzzles if len(p) >= 81]
    t = time.clock()
    for p in puzzles:
        q = solve(initialize_board(p))
    t = time.clock() - t
    print('Solved ' + str(len(puzzles)) + ' puzzles in ' + str(t) + ' seconds.')
    avg = len(puzzles) / t
    print('Averaging ' + str(avg) + ' puzzles per second.')

if __name__ == '__main__':
    main()

# BENCHMARKS

# boards0.txt
# Solved 76 puzzles in 0.34359 seconds.
# Averaging 221.1938647806979 puzzles per second.

# boards1.txt
# Solved 5000 puzzles in 55.533641 seconds.
# Averaging 90.03551558955049 puzzles per second.

# boards2.txt
# Solved 5000 puzzles in 55.947404 seconds.
# Averaging 89.36965153914916 puzzles per second.

# boards3.txt
# Solved 17 puzzles in 0.06851099999999999 seconds.
# Averaging 248.1353359314563 puzzles per second.

# boards4.txt
# Solved 500 puzzles in 825.438726 seconds.
# Averaging 0.605738480944496 puzzles per second.

# boards5.txt
# Solved 95 puzzles in 67.745096 seconds.
# Averaging 1.4023155270161547 puzzles per second.

# boards6.txt
# Solved 11 puzzles in 0.12351100000000001 seconds.
# Averaging 89.06089336172487 puzzles per second.
