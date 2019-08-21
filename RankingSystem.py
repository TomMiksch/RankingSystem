from sportsreference.ncaaf.teams import Team
from sportsreference.ncaaf.teams import Teams
from sportsreference.ncaaf.schedule import Schedule
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import time
import collections
import csv
import sys
import os

# Start timing
start = time.time()

# Default year if none is given
yearToCalculate = datetime.now().year - 1
if (len(sys.argv) > 1):
    yearToCalculate = sys.argv[1]

# Create output directory
output_dir = str(os.getcwd()) + "/output"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# Variables and whatnot
teams = Teams(year=str(yearToCalculate))
teamRankOrder = collections.OrderedDict()
rank = 1

# Give a bonus for beating a Power 5 Conference team (or Notre Dame)
# Lose points for playing an FCS team, and double those points lost if you lose
# Get some bonus points for playing higher ranked opponents, and even more for winning
def gameByGame(team):
    team_schedule = Schedule(team.abbreviation,year=str(yearToCalculate))
    power_5_win_score = 0
    fcs_games_played_score = 0
    opp_rank_score = 0
    for game in team_schedule:
        opp_conference = game.opponent_conference
        if (opp_conference == 'ACC' or
            opp_conference == 'Big Ten' or
            opp_conference == 'SEC' or
            opp_conference == 'Pac-12' or
            opp_conference == 'Big 12' or
            game.opponent_abbr == 'notre-dame'):
            if (game.result == 'Win'):
                power_5_win_score = power_5_win_score + 1
        if (opp_conference == 'Non-DI School'):
            fcs_games_played_score = fcs_games_played_score + 1
            if (game.result == 'Loss'):
                fcs_games_played_score = fcs_games_played_score + 1
        if (game.opponent_rank != None):
            opp_rank_score = opp_rank_score + ((51 - game.opponent_rank) / 50)
            if (game.result == 'Win'):
                opp_rank_score = opp_rank_score + ((51 - game.opponent_rank) / 50)

    return [(power_5_win_score * .3), (fcs_games_played_score * .09), (opp_rank_score * .1)]

# Basic formula to scrape sports-reference
# Team is the team being analyzed
# criteria is the data-stat to be scraped
# wanted_row is Offense(0), Defense(1), or Difference(2)
def scrapeFormula(team, criteria, wanted_row):
    teamNameLowerCase = team.abbreviation

    url = "https://www.sports-reference.com/cfb/schools/" + \
        teamNameLowerCase.lower() + "/" + str(yearToCalculate) + ".html"
    page = urlopen(url).read()

    soup = BeautifulSoup(page, features="lxml")
    table = soup.find("tbody")
    count = 0

    rows = table.find_all('tr')
    for row in rows:
        cell = row.find("td", {"data-stat": str(criteria)})
        if (cell != None and count == wanted_row):
            a = cell.text.strip().encode()
            text = a.decode("utf-8")
        
        count = count + 1

    result = float(text)

    return result

# Gather the YPG allowed by each team
def scrapeYPGDiff(team):
    return scrapeFormula(team, "tot_yds", 2)

# Gather the turnover difference
def scrapeTurnoverBattle(team):
    turnover_diff = scrapeFormula(team, "turnovers", 2)

    return turnover_diff * -1

# Calculate the ranking score for each team
def calculateRankScore(team):
    schedule_score = gameByGame(team)
    calc_wins = (team.wins + schedule_score[0] - schedule_score[1] + schedule_score[2]) * .2
    ypg_diff = scrapeYPGDiff(team) * .01
    ppg_diff = (team.points_per_game - team.points_against_per_game) * .15
    turnover_diff = scrapeTurnoverBattle(team) * .07
    total = calc_wins + ypg_diff + ppg_diff + turnover_diff
    print(team.abbreviation + "'s score: " + str(total))
    return total

# Main function
for team in teams:
    teamRankOrder[team.name] = [team.name, str(team.conference).upper(), calculateRankScore(team)]

# Write results to output file
with open(output_dir + "/rankings_" + str(yearToCalculate) + ".csv", "w") as outfile:
    csvwriter = csv.writer(outfile, delimiter=",", lineterminator="\n")
    for row_cells in teamRankOrder.values():
        csvwriter.writerow(row_cells)

# End timing and output how long it took
stop = time.time()
totalMinutes = ((stop - start)/60)
remainingSeconds = (stop - start) % 60
print('runtime - %.0f:%02.0f' % (totalMinutes, remainingSeconds))
