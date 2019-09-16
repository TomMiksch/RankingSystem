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

args = parser.parse_known_args()
currentYear = args[0].currentYear
week = args[0].week

# Create output directory
output_dir = str(os.getcwd()) + "/output"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# OrderedDict to track everything for CSV
gameTracker = collections.OrderedDict()

# Get the winning team name
def compareTeams(winner, loser, difference, counter):

    with open("output\\winners_" + str(currentYear) + "_week_" + str(week) + ".csv", "r") as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:            
            if (row[0] == winner):
                correct_winner = True

                predicted = row[2]
                if (predicted == None or predicted == ""):
                    predicted = 0
                
                differential = float(predicted) - difference

            if (row[0] == loser):
                correct_winner = False

                predicted = row[2]
                if (predicted == None or predicted == ""):
                    predicted = 0

                predicted = float(predicted) * -1
                
                differential = float(predicted) - difference

    gameTracker[counter] = [winner, loser, predicted, difference, differential, correct_winner]

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

                winner_score = row.find("td", {"data-stat": "winner_points"})
                a = winner_score.text.strip().encode()
                winner_score = a.decode("utf-8")

                loser_score = row.find("td", {"data-stat": "loser_points"})
                a = loser_score.text.strip().encode()
                loser_score = a.decode("utf-8")

                difference = int(winner_score) - int(loser_score)
        
                compareTeams(winner_name, loser_name, difference, counter)

                counter = counter + 1

getScrapeUrl()

with open(output_dir + "/prediciton_vs_actual_" + str(currentYear) + "_week_" + str(week) + ".csv", "w") as outfile:
    csvwriter = csv.writer(outfile, delimiter=",", lineterminator="\n")
    csvwriter.writerow(["WINNER", "LOSER", "PREDICTED", "ACTUAL", "DIFFERENCE", "ACCURATE PREDICTION?"])
    for row_cells in gameTracker.values():
        csvwriter.writerow(row_cells)

# End timing and output how long it took
stop = time.time()
totalMinutes = ((stop - start)/60)
remainingSeconds = (stop - start) % 60
print('runtime - %.0f:%02.0f' % (totalMinutes, remainingSeconds))

