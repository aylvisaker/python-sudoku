import time
import sys
import math
import gmpy2
import itertools
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
import sudoku

def cross(x, y):
    return [a + b for a in x for b in y]

digits = '123456789'
squares = list(range(81))
the_rows = [squares[9*n:9*n+9] for n in range(9)]
the_columns = [squares[n:81:9] for n in range(9)]
corners = [0,3,6,27,30,33,54,57,60]
the_boxes = [squares[n:n+3] + squares[n+9:n+12] + squares[n+18:n+21] for n in corners]
the_groups = the_rows + the_columns + the_boxes

neighborhoods = [[set(g) for g in the_groups if s in g] for s in squares]
neighbors = [list(set([i for nbhd in neighborhoods[s] for i in nbhd]) - {s}) for s in squares]
setneighbors = [set(neighbors[s]) for s in squares]

tuples = [[] for n in range(10)]
for x in range(2**9):
    p = gmpy2.popcount(x)
    tuples[p].append(x)
singles = tuples[1]

values = dict((v, list({s & v for s in singles} - {0})) for v in range(2**9))
valuesets = dict((v, {s & v for s in singles} - {0}) for v in range(2**9))

methodnames = ['naked singles', 'naked doubles', 'hidden singles', 'hidden doubles', 'hidden triples', 'hidden quadruples']
methodcounter = [0 for dummy in methodnames]

def initialize(v):
    global methodcounter
    methodcounter = [0 for dummy in methodnames]
    b = {s: 511 for s in squares}
    for s in squares:
        if v[s] in digits:
            fillin(b, s, 2 ** (int(v[s]) - 1))
    return b

def eliminate(b, s, n):
    global methodcounter
    complement = 511 - n
    candidates = b[s]
    newcandidates = complement & candidates
    if not candidates == newcandidates:
        # update s
        b[s] = newcandidates
        # 0. check for naked singles
        if newcandidates in singles:
            method = 0
            for square in neighbors[s]:
                methodcounter[method] += 1
                eliminate(b, square, b[s])
        # 1. check for naked doubles
        if newcandidates in tuples[2]:
            method = 1
            for square in neighbors[s]:
                if b[square] == newcandidates:
                    nghbrs = setneighbors[s] & setneighbors[square]
                    for i in range(len(nghbrs)):
                        nghbr = nghbrs.pop()
                        for v in values[newcandidates]:
                            methodcounter[method] += 1
                            eliminate(b, nghbr, v)
        # check for hidden tuples
        for nbhd in neighborhoods[s]:
            locations = {sqr for sqr in nbhd if not n & b[sqr] == 0}
            # 2. singles
            if len(locations) == 1:
                method = 2
                methodcounter[method] += 1
                fillin(b, locations.pop(), n)
            # 3. doubles
            if len(locations) == 2:
                method = 3
                x, y = list(locations)
                xvals, yvals = valuesets[x], valuesets[y]
                common = (xvals & yvals) - {n}
                union = (xvals | yvals) - {n}
                # don't bother with naked doubles
                if not len(common) == 1:
                    while common:
                        v = common.pop()
                        vlocations = {sqr for sqr in nbhd if not v & b[sqr] == 0}
                        if vlocations == locations:
                            union.remove(v)
                            while union:
                                s = union.pop()
                                for sqr in [x, y]:
                                    methodcounter[method] += 1
                                    eliminate(b, sqr, s)
            # 4. triples
            if len(locations) == 3:
                method = 4
                x, y , z = list(locations)
                xvals, yvals, zvals = valuesets[x], valuesets[y], valuesets[z]
                common = (xvals & yvals & zvals) - {n}
                union = (xvals | yvals | zvals) - {n}
                # don't bother with naked triples
                if not len(common) < 3:
                    while common:
                        v = common.pop()
                        vlocations = {sqr for sqr in nbhd if not v & b[sqr] == 0}
                        if vlocations == locations and not len(common) == 0:
                            w = common.pop()
                            wlocations = {sqr for sqr in nbhd if not w & b[sqr] == 0}
                            if wlocations == locations:
                                union.remove(v)
                                union.remove(w)
                                while union:
                                    s = union.pop()
                                    for sqr in [x, y, z]:
                                        methodcounter[method] += 1
                                        eliminate(b, sqr, s)
            # 5. quadruples
            if len(locations) == 4:
                method = 5
                w, x, y, z = list(locations)
                wvals, xvals, yvals, zvals = valuesets[w], valuesets[x], valuesets[y], valuesets[z]
                common = (wvals & xvals & yvals & zvals) - {n}
                union = (wvals | xvals | yvals | zvals) - {n}
                # don't bother with naked quadruples
                if not len(common) < 4:
                    while common:
                        p = common.pop()
                        plocations = {sqr for sqr in nbhd if not q & b[sqr] == 0}
                        if plocations == locations and not len(common) == 0:
                            q = common.pop()
                            qlocations = {sqr for sqr in nbhd if not q & b[sqr] == 0}
                            if qlocations == locations and not len(common) == 0:
                                r = common.pop()
                                rlocations = {sqr for sqr in nbhd if not r & b[sqr] == 0}
                                if rlocations == locations:
                                    union.remove(p)
                                    union.remove(q)
                                    union.remove(r)
                                    while union:
                                        s = union.pop()
                                        for sqr in [x, y, z]:
                                            methodcounter[method] += 1
                                            eliminate(b, sqr, s)
            # 6. pointing tuples
            #
    return b

def fillin(b, s, n):
    global methodcounter
    candidates = b[s]
    needseliminated = [x for x in singles if candidates & n == n and not x == n]
    for e in needseliminated:
        eliminate(b, s, e)
    return b

def display(b):
    def f(s):
        if b[s] in singles:
            return str(int(math.log(b[s], 2) + 1))
        else:
            return '+'
    return ''.join([f(s) for s in squares])

def main():
    global methodcounter
    stats = methodcounter
    filenames = ['boards5000.1.txt']
    if len(sys.argv) == 2:
        filenames = [sys.argv[1]]
    for name in filenames:
        file = open(name, 'r')
        puzzles = file.readlines()
        puzzles = [p[:81] for p in puzzles if len(p) >= 81]
        e, c, t = 0, 0, time.clock()
        for p in puzzles:
            methodcounter = [0 for dummy in methodnames]
            q = display(initialize(p))
            r = sudoku.display(sudoku.solve(sudoku.initialize_board(p)))
            if q == r:
                for i in range(6):
                    stats[i] += methodcounter[i]
            else:
                c += 1
                # print(q)
                for s in squares:
                    if not q[s] in [r[s], '+']:
                        e += 1
                        print(r)
        n = len(puzzles)
        t = time.clock() - t
        avg = len(puzzles) / t
        print('\n# ' + name)
        print('# Failed to solve ' + str(c) + ' puzzles. Witnessed ' + str(e) + ' errors.')
        print('# Worked ' + str(n) + ' puzzles in ' + str(t) + ' seconds.')
        print('# Averaging ' + str(avg) + ' puzzles per second.\n')
        print(stats)

if __name__ == '__main__':
    main()
