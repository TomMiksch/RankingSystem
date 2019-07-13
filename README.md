# RankingSystem
Playing with Python to create a college football ranking system

Teaching it to myself so forgive me for any bad code

Created using Python 3.7 and a package called sportsreference, [linked here](https://sportsreference.readthedocs.io/en/latest/index.html)

Web scraping made possible thanks to [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

Huge thank you to Sumedha Mehta, [whose article here helped teach me how to scrape some data](https://medium.com/@smehta/scrape-and-create-your-own-beautiful-dataset-from-sports-reference-com-using-beautifulsoup-python-c26d6920684e)

## To Run This Program
- Make sure BeautifulSoup and sportsreference are installed

`pip install beautifulsoup4`

`pip install sportsreference`

- Then run the script in your terminal with the year you would like to calculate. Will default to previous year if no year declared

`python RankingSystem.py 2018`

- If you are running this on Python 2.7, replace 

`from urllib.request import urlopen` 

with 

`from urllib2 import urlopen`

That's it so far! It'll print the rankings. A lot is planned but again, it's garbage

Current (simple) calculation puts Clemson first, UConn last, and Iowa ahead of everyone they should be ahead of. I may call this a complete system now.
