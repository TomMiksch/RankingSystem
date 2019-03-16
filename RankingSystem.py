from sportsreference.ncaaf.boxscore import Boxscore
from sportsreference.ncaaf.boxscore import Boxscores
from datetime import datetime

# this is all garbage and doesn't do anything yet
games = Boxscores(datetime(2017, 11, 4))
game = Boxscore("2017-11-04-iowa")
print("Winners on 11 November 2017")
print(game.winning_name)