import argparse
import collections
import csv
import os
import time
import generate_html
from datetime import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup
from sportsipy.ncaaf.schedule import Schedule
from sportsipy.ncaaf.teams import Teams

# Start timing
start = time.time()

# Default year if none is given
parser = argparse.ArgumentParser(description = "Rank FBS Programs")
parser.add_argument("-y","--year", 
    dest="yearToCalculate", 
    required=False, 
    help="Year to rank teams", 
    default=datetime.now().year)
parser.add_argument("-w","--week", 
    dest="week", 
    required=False, 
    help="Week of the rankings",
    type=int,
    default=0)

args = parser.parse_known_args()
yearToCalculate = args[0].yearToCalculate
week = args[0].week

# Create output directory
output_dir = str(os.getcwd()) + "/output"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# Variables and whatnot
teams = Teams(year=str(yearToCalculate))
teamRankOrder = collections.OrderedDict()
previousRankings = collections.OrderedDict()

def getPreviousWeeksRankings(previousWeek):
    with open("output\\rankings_" + str(yearToCalculate) + "_week_" + str(previousWeek) + ".csv", "r") as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            previousRankings[row[1]] =  row[5]

# Give a bonus for beating a Power 5 Conference team (or Notre Dame)
# Lose points for playing an FCS team, and double those points lost if you lose
# Get some bonus points for playing higher ranked opponents, and even more for winning
# Does not count games that were not played
def gameByGame(team):
    team_schedule = Schedule(team.abbreviation,year=str(yearToCalculate))
    # power_5_win_score = 0
    # fcs_games_played_score = 0
    # opp_rank_score = 0
    sos_score = 0
    game_played = 0
    opponent = 0
    for game in team_schedule:
        # Get opponent name
        opponent = previousRankings.get(game.opponent_name)
        # Get opponent rank from previous week
            # Either as a variable at the start or straight from the CSV
        if (opponent == None):
            opponent = -4
        if (game.result == "Win"):
            game_played = game_played + 1
            sos_score = sos_score + float(opponent) + (1.3 ** float(opponent))
            
        elif (game.result == "Loss"):
            game_played = game_played + 1
            sos_score = sos_score + float(opponent) - (1.3 ** (-1 * float(opponent)))

    return sos_score / game_played

# Basic formula to scrape sports-reference
# Team is the team being analyzed
# criteria is the data-stat to be scraped
# wanted_row is Offense(0), Defense(1), or Difference(2)
def scrapeFormula(team):
    teamNameLowerCase = team.abbreviation
    ypg_diff = "1"
    turnover_diff = "1"

    url = "https://www.sports-reference.com/cfb/schools/" + \
        teamNameLowerCase.lower() + "/" + str(yearToCalculate) + ".html"
    page = urlopen(url).read()

    soup = BeautifulSoup(page, features="lxml")
    all_team = soup.find("div", {"id": "all_team"})
    table = all_team.find("tbody")
    count = 0

    rows = table.find_all('tr')
    for row in rows:
        ypg_diff_cell = row.find("td", {"data-stat": "tot_yds"})
        turnover_diff_cell = row.find("td", {"data-stat": "turnovers"})
        if (ypg_diff_cell != None and count == 2):
            a = ypg_diff_cell.text.strip().encode()
            ypg_diff = a.decode("utf-8")
        if (turnover_diff_cell != None and count == 2):
            a = turnover_diff_cell.text.strip().encode()
            turnover_diff = a.decode("utf-8")
        
        count = count + 1

    return [float(ypg_diff), float(turnover_diff)]

# Gather the YPG allowed by each team
# def scrapeYPGDiff(team):
#     return scrapeFormula(team, "tot_yds", 2)

# # Gather the turnover difference
# def scrapeTurnoverBattle(team):
#     turnover_diff = scrapeFormula(team, "turnovers", 2)

#     return turnover_diff * -1

# Calculate the ranking score for each team
def calculateRankScore(team):
    getPreviousWeeksRankings(week - 1)
    strength_of_schedule = gameByGame(team)
    ppg_diff = (team.points_per_game - team.points_against_per_game) * .15
    diff_scraper = scrapeFormula(team)
    ypg_diff = diff_scraper[0] * .01
    turnover_diff = diff_scraper[1] * -.07
    total = strength_of_schedule + ypg_diff + ppg_diff + turnover_diff
    print(team.name + "'s score: " + str(total))
    return total

# Main function
for team in teams:
    teamRankOrder[team.name] = [team.name, str(team.conference).upper(), team.wins, team.losses, calculateRankScore(team)]


teamRankOrderSorted = sorted(teamRankOrder.items(), key=lambda x: x[1][4], reverse=True)

# Write results to output file
with open(output_dir + "/rankings_" + str(yearToCalculate) + "_week_" + str(week) + ".csv", "w") as outfile:
    csvwriter = csv.writer(outfile, delimiter=",", lineterminator="\n")
    counter = 1
    csvwriter.writerow(["RANK", "TEAM", "CONFERENCE", "WINS", "LOSSES", "POINTS"])
    for row_cells in teamRankOrderSorted:
        csvwriter.writerow([counter, row_cells[1][0], row_cells[1][1], row_cells[1][2], row_cells[1][3], row_cells[1][4]])
        counter = counter + 1

generate_html.generateHTML(yearToCalculate, week, teamRankOrderSorted)

# End timing and output how long it took
stop = time.time()
totalMinutes = ((stop - start)/60)
remainingSeconds = (stop - start) % 60
print('runtime - %.0f:%02.0f' % (totalMinutes, remainingSeconds))
