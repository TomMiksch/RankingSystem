## [Please visit my github webpage for this project!](https://tommiksch.github.io/RankingSystem/)

# RankingSystem
Playing with Python to create a college football ranking system

Teaching it to myself so forgive me for any bad code

Created using Python 3.7 and a package called sportsreference, [linked here](https://sportsreference.readthedocs.io/en/latest/index.html)

Web scraping made possible thanks to [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

Huge thank you to Sumedha Mehta, [whose article here helped teach me how to scrape some data](https://medium.com/@smehta/scrape-and-create-your-own-beautiful-dataset-from-sports-reference-com-using-beautifulsoup-python-c26d6920684e)

## To Run The Ranking System
- Make sure BeautifulSoup and sportsreference are installed

`pip install beautifulsoup4`

`pip install sportsreference`

- Then run the script in your terminal with the year and week you would like to calculate. Will default to previous year if no year declared. Year can be declared as `-y=XXXX` or `--year=XXXX`, week can be referenced as `-w=X` or `--week=X`

`python RankingSystem.py -y=2018 -w=4`

- If you are running this on Python 2.7, replace 

`from urllib.request import urlopen` 

with 

`from urllib2 import urlopen`

Current (simple) calculation puts Clemson first, UConn last, and Iowa ahead of everyone they should be ahead of. I may call this a complete system now.

## To Run The Weekly Winners Script
- Make sure BeautifulSoup and sportsreference are installed as above

- Sports-Reference counts what most people refer to as "Week 0" as "Week 1" and that is reflected the use of this script

- Run the script in terminal with the season and week you'd like to predict. For example, to run the rankings on Week 2 of the 2019 season, enter

`python weekly_winners.py -y=2019 -w=2`

into your terminal

- Output will be written to a csv file in the output folder

## To Run The Results Script
- This script will check the predictions from the week before compared to the actual results

- Run the script in your terminal with the year and week you want to check as

`python results.py -y=2019 -w=4`

- Output will be written to a csv file in the output folder
