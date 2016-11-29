import time
import sys
# import random

# Tools and Constants


def cross(x, y):
    return [a + b for a in x for b in y]

specials = '.+0'
digits = '123456789'
blocks = ['123', '456', '789']
squares = cross(digits, digits)
the_rows = [cross(x, digits) for x in digits]
the_columns = [cross(digits, x) for x in digits]
the_boxes = [cross(x, y) for x in blocks for y in blocks]
the_groups = the_rows + the_columns + the_boxes
neighborhoods = dict((s, [g for g in the_groups if s in g]) for s in squares)
neighbors = dict((s, set([i for nbhd in neighborhoods[s] for i in nbhd]) - {s}) for s in squares)


def initialize_board(v):
    b = {s: digits for s in squares}
    for i, s in enumerate(squares):
        if v[i] not in specials:
            fillin(b, s, v[i])
    return b


def eliminate(b, s, n):
    if not(n in b[s]):
        return b
    b[s] = b[s].replace(n, '')
    if len(b[s]) == 0:
        return False
    # Naked singles
    if len(b[s]) == 1:
        if not all(eliminate(b, r, b[s]) for r in neighbors[s]):
            return False
    for nbhd in neighborhoods[s]:
        locations = [sq for sq in nbhd if n in b[sq]]
        # Nowhere to put 'n' in this neighborhood
        if len(locations) == 0:
            return False
        # Hidden singles
        if len(locations) == 1:
            if not fillin(b, locations[0], n):
                return False
    return b


def fillin(b, s, n):
    leftover = b[s].replace(n, '')
    if all(eliminate(b, s, x) for x in leftover):
        return b
    return False


def solve(b):
    if b is False:
        return False
    if all(len(b[s]) == 1 for s in squares):
        return b
    s = min((len(b[s]), s) for s in squares if len(b[s]) > 1)[1]
    candidates = b[s]  # ''.join(random.sample(b[s], len(b[s])))
    for cand in candidates:
        d = solve(fillin(b.copy(), s, cand))
        if d:
            return d


def display(b):
    if b is False:
        return False
    line = ''
    for s in squares:
        x = b[s]
        if len(x) == 1:
            line += x
        else:
            line += specials[0]
    return(line)


def main():
    file_names = ['puzzles/singlesonly.txt']
    if len(sys.argv) == 2:
        file_names = [sys.argv[1]]
    for name in file_names:
        file = open(name, 'r')
        puzzles = file.readlines()
        puzzles = [p[:81] for p in puzzles if len(p) >= 81]
        t = time.clock()
        for p in puzzles:
            q = solve(initialize_board(p))
            # q = initialize_board(p)
            # if q == solve(q):
            #     print(p)
        t = time.clock() - t
        avg = len(puzzles) / t
        print('# ' + name)
        print('# Solved ' + str(len(puzzles)) + ' puzzles in ' + str(t) + ' seconds.')
        print('# Averaging ' + str(avg) + ' puzzles per second.\n')

if __name__ == '__main__':
    main()