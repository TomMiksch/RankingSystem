from sportsreference.ncaaf.boxscore import Boxscore
from sportsreference.ncaaf.boxscore import Boxscores
from sportsreference.ncaaf.teams import Team
from sportsreference.ncaaf.teams import Teams
from sportsreference.ncaaf.schedule import Schedule
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import collections

# Start timing
start = time.time()

teams = Teams()
teamRankOrder = collections.OrderedDict()
rank = 1

# Gather the YPG allowed by each team
def calcDefYPG(team):
    teamNameLowerCase = team.abbreviation

    url = "https://www.sports-reference.com/cfb/schools/" + \
        teamNameLowerCase.lower() + "/2018.html"
    page = urlopen(url).read()

    soup = BeautifulSoup(page, features="lxml")
    table = soup.find("tbody")
    yards_given_up_per_game = {'opp_tot_yds'}

    rows = table.find_all('tr')
    for row in rows:
        for y in yards_given_up_per_game:
            cell = row.find("td",{"data-stat": y})
            if (cell != None):
                a = cell.text.strip().encode()
                text = a.decode("utf-8")

    total_yards = float(text)

    return total_yards

# Calculate the ranking score for each team
def calculateRankScore(team):
    calc_wins = (team.wins + team.conference_wins) * .2
    ypg_diff = (team.yards - calcDefYPG(team)) * .01
    total = calc_wins + ypg_diff
    print(team.name + "'s score - " + str(total))
    return total

# Main function
for team in teams:
    teamRankOrder[team.name] = calculateRankScore(team)

# Output results
for key, value in sorted(teamRankOrder.items(), key=lambda item: item[1], reverse=True):
    print('%s. %s: %s' % (rank, key, value))
    rank = rank + 1

# End timing and output how long it took
stop = time.time()
totalTime = stop - start
print('took %.2f seconds' % totalTime)
