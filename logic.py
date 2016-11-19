import time
import sys
import math
import sudoku
from gmpy import popcount

def cross(x, y):
    return [a + b for a in x for b in y]

digits = '123456789'
squares = list(range(81))
the_rows = [squares[9*n:9*n+9] for n in range(9)]
the_columns = [squares[n:81:9] for n in range(9)]
the_boxes = [squares[n:n+3] + squares[n+9:n+12] + squares[n+18:n+21] for n in [0,3,6,27,30,33,54,57,60]]
the_groups = the_rows + the_columns + the_boxes

neighborhoods = [[g for g in the_groups if s in g] for s in squares]
neighbors = [list(set([i for nbhd in neighborhoods[s] for i in nbhd]) - {s}) for s in squares]

tuples = [[x for x in range(512) if popcount(x) == n] for n in range(10)]
singles = tuples[1]

def initialize(v):
    b = {s: 511 for s in squares}
    for s in squares:
        if v[s] in digits:
            fillin(b, s, 2 ** (int(v[s]) - 1))
    return b


def eliminate(b, s, n):
    complement = 511 - n
    candidates = b[s]
    newcandidates = complement & candidates
    if not candidates == newcandidates:
        b[s] = newcandidates
        # check for naked singles
        if b[s] in singles:
            for square in neighbors[s]:
                eliminate(b, square, b[s])
        # check for hidden singles
        for nbhd in neighborhoods[s]:
            locations = [sqr for sqr in nbhd if not n & b[sqr] == 0]
            if len(locations) == 1:
                fillin(b, locations[0], n)
    return b


def fillin(b, s, n):
    candidates = b[s]
    needseliminated = [x for x in singles if not x == n]
    for e in needseliminated:
        eliminate(b, s, e)
    return b


def display(b):
    return ''.join([str(int(math.log(b[s], 2) + 1)) for s in squares])


def main():
    filenames = ['singlesonly.txt']
    if len(sys.argv) == 2:
        filenames = [sys.argv[1]]
    for name in filenames:
        file = open(name, 'r')
        puzzles = file.readlines()
        puzzles = [p[:81] for p in puzzles if len(p) >= 81]
        t = time.clock()
        for p in puzzles:
            q = initialize(p)
            # print(display(q))
        n = len(puzzles)
        t = time.clock() - t
        avg = len(puzzles) / t
        print('# ' + name)
        print('# Solved ' + str(n) + ' puzzles in ' + str(t) + ' seconds.')
        print('# Averaging ' + str(avg) + ' puzzles per second.\n')

if __name__ == '__main__':
    main()
