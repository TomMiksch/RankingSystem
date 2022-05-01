import collections
import os
import time
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Start timing
start = time.time()

# Variables and whatnot
year = 2022
endYear = 1936


def getInitialSet():
    print('Initial Set Begin')

    init_set = set()
    init_dict = collections.OrderedDict()

    url = "https://www.pro-football-reference.com/schools/"
    page = urlopen(url).read()

    soup = BeautifulSoup(page, features="lxml")
    draft_board = soup.find("div", {"id": "div_college_stats_table"})
    table = draft_board.find("tbody")

    rows = table.find_all('tr')
    for row in rows:
        college_cell = row.find("td", {"data-stat": "college_name"})
        if (college_cell != None):
            a = college_cell.text.strip().encode()
            college_text = a.decode("utf-8")
            init_set.add(college_text)
            init_dict[college_text] = 3000

    print('Initial Set End')
    return [init_set, init_dict]

def getColleges(year, init_set, init_dict):
    print(str(year) + ' Begin')
    year_set = set()

    url = "https://www.pro-football-reference.com/years/" + str(year) + "/draft.htm"
    page = urlopen(url).read()

    soup = BeautifulSoup(page, features="lxml")
    draft_board = soup.find("div", {"id": "div_drafts"})
    table = draft_board.find("tbody")

    rows = table.find_all('tr')
    for row in rows:
        college_cell = row.find("td", {"data-stat": "college_id"})
        if (college_cell != None):
            a = college_cell.text.strip().encode()
            college_text = a.decode("utf-8")
            year_set.add(college_text)

    final_set = init_set.intersection(year_set)

    for school in final_set:
        init_dict[school] = year

    print(str(year) + ' End')
    return [final_set, init_dict]

init_data = getInitialSet()
init_set = init_data[0]
init_dict = init_data[1]
result_set = init_set
result_dict = init_dict

while year >= endYear or len(init_set) == 0:
    data = getColleges(year, result_set, result_dict)
    result_set = data[0]
    result_dict = data[1]
    year = year - 1

sorted = sorted(result_dict.items(), key = lambda t: t[1])

for item in sorted:
    consecutive = (2022 - item[1]) + 1
    print('[' + item[0] + '](#f/' + item[0].replace(' ', '').replace('st.', 'state').lower() + ') | ' + str(item[1]) + ' | ' + str(consecutive))

# End timing and output how long it took
stop = time.time()
totalMinutes = ((stop - start)/60)
remainingSeconds = (stop - start) % 60
print('runtime - %.0f:%02.0f' % (totalMinutes, remainingSeconds))
