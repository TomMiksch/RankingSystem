from sportsreference.ncaaf.boxscore import Boxscore
from sportsreference.ncaaf.boxscore import Boxscores
from sportsreference.ncaaf.teams import Team
from sportsreference.ncaaf.teams import Teams
from sportsreference.ncaaf.schedule import Schedule
from datetime import datetime
import time
import collections

# Start timing
start = time.time()

teams = Teams()
teamRankOrder = collections.OrderedDict()
rank = 1

# Calculate the YPG allowed by each team
def calcDefYPG( team ):
    print(team.name)
    team_schedule = Schedule(team.name)
    total_yards = 0

    for game in team_schedule:
        # Get YPG allowed if game is home
        if game.location == 'home':
            print('game.away_total_yards ' + str(game.away_total_yards))
            total_yards = total_yards + game.away_total_yards
            
        # Get YPG allowed if game is away
        # Get YPG allowed if game is neutral
    return total_yards

# Calculate the ranking score for each team
def calculateRankScore( team ):
    calc_wins = team.wins + team.conference_wins
    ypg_diff = team.yards - calcDefYPG(team)
    total = calc_wins / ypg_diff
    return total

# Main function
for team in teams:
    teamRankOrder[team.name] = calculateRankScore(team)

# Output results
for key, value in sorted(teamRankOrder.items(), key=lambda item: item[1], reverse = True):
    print("%s. %s: %s" % (rank, key, value))
    rank = rank + 1

# End timing and output how long it took
stop = time.time()
totalTime = stop - start
print("took %.2f seconds" % totalTime)