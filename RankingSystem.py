from sportsreference.ncaaf.boxscore import Boxscore
from sportsreference.ncaaf.boxscore import Boxscores
from sportsreference.ncaaf.teams import Team
from sportsreference.ncaaf.teams import Teams
from datetime import datetime
import time
import collections

# this is all garbage and doesn't do anything yet
start = time.time()

teamRankOrder = collections.OrderedDict()

teams = Teams()
for team in teams:
    teamRankOrder[team.name] = team.wins

for key, value in sorted(teamRankOrder.items(), key=lambda item: item[1], reverse = True):
    print("%s: %s" % (key, value))

stop = time.time()

print("took " + str(stop - start) + " seconds")