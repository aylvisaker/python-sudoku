import time
import random
# import gmpy2

base = 4
allsymbols = ''.join(chr(i) for i in range(32, 128))
start = 17
digits = allsymbols[start:start + base**2]
specials = ''.join(allsymbols[i] for i in [14, 16])
blocks = [digits[base*i: base*i + base] for i in range(base)]


def cross(A,B):
    return [a + b for a in A for b in B]

squares = cross(digits, digits)
therows = [cross(x, digits) for x in digits]
thecolumns = [cross(digits, x) for x in digits]
theboxes = [cross(x, y) for x in blocks for y in blocks]
thegroups = therows + thecolumns + theboxes

neighborhoods = dict((s, [g for g in thegroups if s in g]) for s in squares)
neighbors = dict((s, set([i for nbhd in neighborhoods[s] for i in nbhd]) - {s}) for s in squares)
index = dict((squares[i], i) for i in range(base**4))


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
    for neighborhood in neighborhoods[s]:
        places = [s for s in neighborhood if n in b[s]]
        if len(places) == 0:
            return False
        elif len(places) == 1:
            if not fillin(b, places[0], n):
                return False
    return b


def solve(b):
    if b is False:
        return False
    elif all(len(b[s]) == 1 for s in squares):
        return b
    else:
        candidacy = list((len(b[s]), s) for s in squares if len(b[s]) > 1)
        i, s = min(candidacy)
        candidates = ''.join(random.sample(b[s], len(b[s])))
        for cand in candidates:
            d = b.copy()
            d = fillin(d, s, cand)
            d = solve(d)
            if d:
                return d


def count(b, solution):
    if not solution:
        return 0
    for s in squares:
        if len(b[s]) > 1:
            d = b.copy()
            d[s] = d[s].replace(solution[s], '')
            if solve(d):
                return 2
    return 1


def display(b):
    if b is False:
        return False
    line = ''
    for s in squares:
        if len(b[s]) == 1:
            line += b[s]
        else:
            line += '0'
    return(line)


def generate17():
    blank = initialize_board('0' * base**4)
    solution = solve(blank.copy())
    unchecked = squares.copy()
    empties, fulls = [], squares.copy()
    while unchecked:
        targetfreedom = min(len(set(neighbors[s]) & set(fulls)) for s in unchecked)
        pot = [s for s in unchecked if len(set(neighbors[s]) & set(fulls)) == targetfreedom]
        s = random.choice(pot)
        ## freedom = dict()
        ## for s in unchecked:
        ##    d = blank.copy()
        ##    for square in fulls:
        ##        if square != s:
        ##            d = fillin(d, square, solution[square])
        ##    freedom[s] = (len(d[s]), s)
        ## f, s = max(freedom[s] for s in unchecked)
        unchecked.remove(s)
        fulls.remove(s)
        d = blank.copy()
        for square in fulls:
            d = fillin(d, square, solution[square])
        if count(d, solution) == 1:
            empties += [s]
        else:
            fulls += [s]
    for square in fulls:
        blank[square] = solution[square]
    return blank

def test(file):
    t, n = time.clock(), 0
    puzzles = open(file, 'r')
    for line in puzzles:
        n += 1
        puzzle, solution = line[0:81], line[83:164]
        computed = display(solve(initialize_board(puzzle)))
        if computed != solution:
            print('error solving puzzle: ' + puzzle)
    t = time.clock() - t
    print('solved {} puzzles in {} seconds'.format(n, t))


# test('su17ExtremeDiff500.txt')
for i in range(10000):
    # random.seed('stuff and junk' + str(i))
    v = display(generate17())
    b = initialize_board(v)
    s = solve(b.copy())
    print(display(s))
    n = count(b, s)
    c = len(v.replace('0',''))
    if c < 256: 
        print('{} clue puzzle generated: {} {} solutions found.'.format(c, v, n))
