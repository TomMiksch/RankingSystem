from sportsreference.ncaaf.teams import Teams
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sys
import csv
import os

# Start timing
start = time.time()

# Default year if none is given, along with week
currentYear = datetime.now().year - 1
week = 1
rank_year = datetime.now().year - 1
if (len(sys.argv) > 3):
    currentYear = sys.argv[1]
    week = sys.argv[2]
    rank_year = sys.argv[3]

    

teams = Teams(year=str(currentYear))

# Get the winning team name
def compareTeams(team1, team2):
    winner_score = None
    loser_score = None
    team1_abbr = None
    team2_abbr = None

    for team in teams:
        # print(team1.replace(" ", "-").upper() + " " + str(team.abbreviation))
        if (team1 == str(team.name) or team1.lower() == str(team.abbreviation.replace("-", " ").lower())):
            team1_abbr = team.name

        elif (team2 == str(team.name) or team2.lower() == str(team.abbreviation.replace("-", " ").lower())):
            team2_abbr = team.name

    with open("output\\rankings_" + currentYear + ".csv", "r") as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if (row[0] == team1_abbr):
                winner_score = float(row[2])
                # print("team1: " + team1_abbr)
                # print(team1_abbr + ": " + str(winner_score))

            if (row[0] == team2_abbr):
                loser_score = float(row[2])
                # print("team2: " + team2_abbr)
                # print(team2_abbr + ": " + str(loser_score))

        if (winner_score == None and loser_score == None):
            print("Neither team found...")

        elif (winner_score == None):
            print("Winner by default: " + team2)

        elif (loser_score == None):
            print("Winner by default: " + team1)

        elif (winner_score > loser_score):
            print("Winner: " + team1 + " Loser: " + team2)

        elif (winner_score < loser_score):
            print("Winner: " + team2 + " Loser: " + team1)

        else:
            print("A FUCKING TIE. GOD DAMMIT " + team1 + ", " + team2)

def getScrapeUrl():
    url = "https://www.sports-reference.com/cfb/years/" + currentYear + "-schedule.html"
    page = urlopen(url).read() 

    soup = BeautifulSoup(page, features="lxml")
    table = soup.find("tbody")

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
                    winner_name = winner_name.split(") ", 1)[0]
                    print(winner_name)

                loser = row.find("td", {"data-stat": "loser_school_name"})
                a = loser.text.strip().encode()
                loser_name = a.decode("utf-8")
                if (loser_name.startswith("(")): 
                    loser_name = loser_name.split(") ", 1)[1]
        
                compareTeams(winner_name, loser_name)

getScrapeUrl()

# End timing and output how long it took
stop = time.time()
totalMinutes = ((stop - start)/60)
remainingSeconds = (stop - start) % 60
print('runtime - %.0f:%02.0f' % (totalMinutes, remainingSeconds))

