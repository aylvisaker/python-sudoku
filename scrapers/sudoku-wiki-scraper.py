import bs4
import urllib.request as url
import time

t = time.clock()
the_file = open('unsolvable.txt', 'w')
puzzle_numbers = range(1, 229)
for puzzle_number in puzzle_numbers:
    address = 'http://www.sudokuwiki.org/feed/scanraid/ASSudokuWeekly.asp?wp=' + str(puzzle_number)
    address = 'http://www.sudokuwiki.org/Print_Weekly_Sudoku.asp?unsolvable=' + str(puzzle_number)
    html = url.urlopen(address)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    puzzle = tables[4]
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