# MetacriticWebscraperandDB
## Description
This repository contains a Python based web scraper and database application interfacing with a SQlite3 database. This project was done as the final project for CS4620: Database Systems at Ohio University

## Files
### Metacritic Page Scraper
metacriticpagescraper.py is a web scraping file that collects URLs. When run the program connects to a Metacritic page that browses all video games ranked by Meta score from highest to lowest in a given year. The program will then scrape the URL for each game's individual page. The years can be easily changed as the program runs using a for loop running from one chosen year to another. The URLs are then saved to a file called gameurls.csv.

### Metacritic Review Scraper
metacriticreviewscraper.py is a web scraping file that collects various data from the review page of a video game. The information collected from each page is the game's title, platform, publisher, release date, Meta score, user score, developer, genres, rating, and cover art. The program reads a games URL, retrieved from gameurls.csv which was made previously using metacriticpagescraper.py. Each URL is read from the file, the program then travels to that page, scrapes the data, and then inserts it into the database. Reviews are scraped by using a for loop which will loop through a selectable number of URLs, starting from 0, or the first URL in gameurls.csv, all the way to 19054, or the latest urls as of December 8, 2021.

### Metacritic Database Application
metacriticdbapp.py is the actual database application file of the Metacritic database. This file provides an interface so that user can easily access the information inside the database without having to enter actual SQLite queries. The program connects to the database an allows provides the user with a menu showing them the options they have for looking up information. The user then presses a number on their keyboard corresponding to the option they want. This then takes the user to another menu with further instructions depending on the first option chosen.

### Metacritic Database
metacriticgames.db is the database file housing all of the data scraped from the game pages on Metacritic.com. The file receives its data from metacriticreveiwscraper.py, and then is interacted with through metacriticdbapp.py. The database is SQLite3 based.

### Metacritic Database Backup
metacriticgamesbackup.db is a backup of the database for emergencies.

## Running the Programs
Running the web scrapers is simple. You only need to run programs and they will do their jobs. If you wish, you can change how much data you want them to collect by changing the values in the loops that control how many times the programs are run.

The application program is also ran by simply running the program. All that is required is that the database and the application program be in the same directory. Otherwise, the application should require no other set up or manipulation to run. 

## Libraries
Multiple 3rd party libraries were used in during this project. They will be needed to run all the programs in this repository. These are all the imported libraries that may need to be installed:
### sqlite3
### pandas
### BeautifulSoup
### requests
### lxml
### html5lib
### matplotlib
### pillow
\
These libraries should come with Python, but will be mentioned as a precaution:
### datetime
### csv
### urllib.request
