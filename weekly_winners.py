from sportsreference.ncaaf.teams import Teams
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import time
import collections
import sys
import csv
import os
import argparse

# Start timing
start = time.time()

# Argument Parser
parser = argparse.ArgumentParser(description = "Pick Weekly Winners")
parser.add_argument("-y","--year", 
    dest="currentYear", 
    required=False, 
    help="Year to rank teams", 
    default=datetime.now().year - 1)
parser.add_argument("-w","--week", 
    dest="week", 
    required=False, 
    help="Week to rank teams", 
    default=1)
parser.add_argument("-r","--rank", 
    dest="rank_year", 
    required=False, 
    help="Set of rankings to use", 
    default=datetime.now().year - 1)

args = parser.parse_known_args()
currentYear = args[0].currentYear
week = args[0].week
rank_year = args[0].rank_year

# Create output directory
output_dir = str(os.getcwd()) + "/output"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# Get all teams
teams = Teams(year=str(rank_year))

# OrderedDict to track everything for CSV
winnerTracker = collections.OrderedDict()

# Get the winning team name
def compareTeams(team1, team2, counter):
    team1_score = None
    team2_score = None
    team1_abbr = None
    team2_abbr = None
    winner = team1
    loser = team2
    differential = None

    for team in teams:
        if (team1 == str(team.name) 
          or team1.replace("-", " ").lower() == str(team.abbreviation.replace("-", " ").lower())):
            team1_abbr = team.name

        elif (team2 == str(team.name) 
          or team2.replace("-", " ").lower() == str(team.abbreviation.replace("-", " ").lower())):
            team2_abbr = team.name

    with open("output\\rankings_" + str(rank_year) + ".csv", "r") as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if (row[0] == team1_abbr):
                team1_score = float(row[2])

            if (row[0] == team2_abbr):
                team2_score = float(row[2]) + .45

        if (team1_score == None and team2_score == None):
            print("Neither " + team1 + " or " + team2 + " found")

        elif (team1_score == None):
            winner = team2
            loser = team1

        elif (team2_score == None):
            # Just to make it clear this case was thought about
            differential = None

        elif (team1_score > team2_score):
            differential = (team1_score - team2_score)/.15

        elif (team1_score < team2_score):
            winner = team2
            loser = team1
            differential = (team2_score - team1_score)/.15

        else:
            differential = (team2_score - team1_score)/.15

    winnerTracker[counter] = [winner, loser, differential]

def getScrapeUrl():
    url = "https://www.sports-reference.com/cfb/years/" + str(currentYear) + "-schedule.html"
    page = urlopen(url).read() 

    soup = BeautifulSoup(page, features="lxml")
    table = soup.find("tbody")

    counter = 0

    rows = table.find_all('tr')
    for row in rows:
        cell = row.find("td", {"data-stat": "week_number"})
        if (cell != None):
            a = cell.text.strip().encode()
            text = a.decode("utf-8")
            if (text == str(week)):
                winner = row.find("td", {"data-stat": "winner_school_name"})
                a = winner.text.strip().encode()
                winner_name = a.decode("utf-8")
                if (winner_name.startswith("(")):
                    winner_name = winner_name.split(")\xa0")[1]

                loser = row.find("td", {"data-stat": "loser_school_name"})
                a = loser.text.strip().encode()
                loser_name = a.decode("utf-8")
                if (loser_name.startswith("(")): 
                    loser_name = loser_name.split(")\xa0")[1]
        
                compareTeams(winner_name, loser_name, counter)

                counter = counter + 1

getScrapeUrl()

with open(output_dir + "/winners_" + str(currentYear) + "_week_" + str(week) + ".csv", "w") as outfile:
    csvwriter = csv.writer(outfile, delimiter=",", lineterminator="\n")
    csvwriter.writerow(["WINNER", "LOSER", "DIFFERENCE"])
    for row_cells in winnerTracker.values():
        csvwriter.writerow(row_cells)

# End timing and output how long it took
stop = time.time()
totalMinutes = ((stop - start)/60)
remainingSeconds = (stop - start) % 60
print('runtime - %.0f:%02.0f' % (totalMinutes, remainingSeconds))

