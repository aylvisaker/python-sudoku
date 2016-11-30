import bs4
import urllib.request as url
import time

# Scrapes hexadoku puzzles from http://www.hexadoku.de/
puzzle_numbers = list(range(1, 3695))
puzzle_numbers.remove(1810)
puzzle_numbers.remove(2252)

t = time.clock()
the_file = open('hex-puzzles.txt', 'w')
for puzzle_number in puzzle_numbers:
    address = 'http://www.hexadoku.de/hexadoku-' + str(puzzle_number) + '.html'
    html = url.urlopen(address)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    tables = soup.findAll('table')
    puzzle = tables[1]
    data = []
    rows = puzzle.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [element.text.strip() for element in cols]
        def f(x):
            if x == '':
                return '+'
            else:
                return x
        cols = ''.join([f(x) for x in cols])
        data.append(cols)
    out = ''.join(data) + '\n'
    the_file.write(out)

print('Downloaded ' + str(puzzle_number) + ' puzzles in ' + str(time.clock() - t) + ' seconds.')