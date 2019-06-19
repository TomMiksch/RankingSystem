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

# Give a bonus for beating a Power 5 Conference team (or Notre Dame)
def power5Wins(team):
    power_5_win_score = 0
    team_schedule = Schedule(team.abbreviation)
    for game in team_schedule:
        if (game.opponent_conference == 'ACC' or
            game.opponent_conference == 'Big Ten' or
            game.opponent_conference == 'SEC' or
            game.opponent_conference == 'Pac-12' or
            game.opponent_conference == 'Big 12' or
            game.opponent_abbr == 'notre-dame'):
            if (game.result == 'Win'):
                power_5_win_score = power_5_win_score + 1

    return (power_5_win_score * .3)

# Lose points for playing an FCS team, and double those points lost if you lose
def fcsGames(team):
    fcs_games_played = 0
    team_schedule = Schedule(team.abbreviation)
    for game in team_schedule:
        if (game.opponent_conference == 'Non-DI School'):
            fcs_games_played = fcs_games_played + 1
        if (game.result == 'Loss'):
            fcs_games_played = fcs_games_played + 1

    return (fcs_games_played * .09)

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
    calc_wins = (team.wins + power5Wins(team) - fcsGames(team)) * .2
    ypg_diff = (team.yards - calcDefYPG(team)) * .01
    ppg_diff = (team.points_per_game - team.points_against_per_game) * .15
    total = calc_wins + ypg_diff + ppg_diff
    print(team.name + "'s score: " + str(total))
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
totalMinutes = ((stop - start)/60)
remainingSeconds = (stop - start) % 60
print('runtime - %.0f:%.0f' % (totalMinutes, remainingSeconds))
