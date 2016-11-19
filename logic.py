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

# TODO try to minimize unnecessary calls to eliminate
# TODO make functions for each separate technique
# TODO add lots of comments
# TODO strange behavior note: in boards5000.1.txt
#       failed 2050 puzzles with [0,1,2,3,4,5,6]
#       failed 2048 puzzles with [0,1,6,2,3,4,5]
#       failed 2048 puzzles with [0,1,2,6,3,4,5]

def cross(x, y):
    return [a + b for a in x for b in y]

digits = '123456789'
squares = list(range(81))
squaresset = set(squares)
the_rows = [squares[9*n:9*n+9] for n in range(9)]
the_columns = [squares[n:81:9] for n in range(9)]
corners = [0,3,6,27,30,33,54,57,60]
the_boxes = [squares[n:n+3] + squares[n+9:n+12] + squares[n+18:n+21] for n in corners]
the_groups = the_rows + the_columns + the_boxes

neighborhoods = [[set(g) for g in the_groups if s in g] for s in squares]
neighbors = [list(set([i for nbhd in neighborhoods[s] for i in nbhd]) - {s}) for s in squares]
setneighbors = [set(neighbors[s]) for s in squares]

coordinates = dict((s, [9,9,9]) for s in squares)
for x in range(9):
    for y in the_rows[x]:
        coordinates[y][0] = x
    for y in the_columns[x]:
        coordinates[y][1] = x
    for y in the_boxes[x]:
        coordinates[y][2] = x

tuples = [[] for n in range(10)]
for x in range(2**9):
    p = gmpy2.popcount(x)
    tuples[p].append(x)
singles = tuples[1]

values = dict((v, list({s & v for s in singles} - {0})) for v in range(2**9))
valuesets = dict((v, {s & v for s in singles} - {0}) for v in range(2**9))

methodnames = ['naked singles', 'naked doubles', 'hidden singles', 'hidden doubles', 'hidden triples',
               'hidden quadruples', 'intersectionremoval']
methodcounter = [0 for dummy in methodnames]

def initialize(v):
    global methodcounter
    # methodcounter = [0 for dummy in methodnames]
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
        size = gmpy2.popcount(x)
        # 0. check for naked singles
        if newcandidates in singles:
            method = 0
            for square in neighbors[s]:
                methodcounter[method] += 1
                eliminate(b, square, newcandidates)
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
        # 7. check for naked triples
        if newcandidates in tuples[2] or newcandidates in tuples[3]:
            method = 7
        # check for hidden tuples
        for nbhd in neighborhoods[s]:
            locations = {sqr for sqr in nbhd if not (n & b[sqr] == 0)}
            locationslist = list(locations)
            # 2. hidden singles
            if len(locations) == 1:
                method = 2
                methodcounter[method] += 1
                fillin(b, locations.pop(), n)
            # 6. intersection removal
            if len(locations) in [2, 3]:
                method = 6
                rw = {coordinates[x][0] for x in locationslist}
                cl = {coordinates[x][1] for x in locationslist}
                bx = {coordinates[x][2] for x in locationslist}
                common_nghbrs = squaresset - setneighbors[s]
                if (len(rw) == len(bx) == 1) or (len(cl) == len(bx) == 1):
                    for x in locationslist:
                        common_nghbrs &= setneighbors[x]
                    while common_nghbrs:
                        x = common_nghbrs.pop()
                        methodcounter[method] += 1
                        eliminate(b, x, n)
            # 3. hidden doubles
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
                            if v in union:
                                union.remove(v)
                            else:
                                print(display(b))
                                print(v, union)
                            while union:
                                s = union.pop()
                                for sqr in [x, y]:
                                    methodcounter[method] += 1
                                    eliminate(b, sqr, s)
            # 4. hidden triples
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
            # 5. hidden quadruples
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
    filenames = ['boards5000.1.txt']
    if len(sys.argv) == 2:
        filenames = [sys.argv[1]]
    for name in filenames:
        file = open(name, 'r')
        puzzles = file.readlines()
        puzzles = [p[:81] for p in puzzles if len(p) >= 81]
        e, c, t = 0, 0, time.clock()
        for p in puzzles:
            q = display(initialize(p))
            r = sudoku.display(sudoku.solve(sudoku.initialize_board(p)))
            if not q == r:
                c += 1
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
        print(methodcounter)

if __name__ == '__main__':
    main()
