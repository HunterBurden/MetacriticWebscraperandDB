#MeteCritic Pagescraper
import requests
import pandas as pd
from bs4 import BeautifulSoup
from PIL import Image
from datetime import datetime
import sqlite3

connection = sqlite3.connect('metacriticgames.db')
db = connection.cursor()
df = pd.read_csv(r"..\MetacriticWebscraperandDB\gameurls.csv")

def page_scraper(game_url, game_id):
    #Getting the URL and setting up the soup page to be scraped
    url = "https://www.metacritic.com" + game_url
    user_agent = {'User-agent': 'Mozilla/5.0'}
    response  = requests.get(url, headers = user_agent)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Getting the Title of the game
    product_title = soup.find("div", class_ = "product_title")
    if(product_title is not None):
        game_title = product_title.find("h1")
        game_title = game_title.text.strip()
    else:
        return

    #Getting the Platform the game is on
    platform = product_title.find("span", class_ = "platform")
    if(platform is not None):
        platform = platform.text.strip()
    else:
        platform = "N/A"

    #Getting the product data elements
    product_data = soup.find("div", class_ = "product_data")

    #Getting the Publisher of the game
    publisher_data = product_data.find("li", class_ = "summary_detail publisher")
    if(publisher_data is not None):
        span = publisher_data.find("span", class_ = "data")
        publisher = span.find("a")
        publisher = publisher.text.strip()
    else:
        publisher = "N/A"

    #Getting the Release Date of the game
    release_data = product_data.find("li", class_ = "summary_detail release_data")
    release_date = release_data.find("span", class_ = "data")
    if(release_date is not None):
        release_date = release_date.text.strip()
        if(release_date == "TBA - Early Access"):
            date = release_date
        else:
            date = datetime.strptime(release_date, '%b %d, %Y').date()
    else:
        date = "N/A"
    
    #Getting the Metascore
    meta_wrap = soup.find("div", class_ = "metascore_wrap highlight_metascore")
    meta_score = meta_wrap.find("span", itemprop = "ratingValue")
    if(meta_score is not None):
        meta_score = meta_score.text.strip()
        int(meta_score)
    else:
        meta_score = 0

    #Getting the User Score
    user_wrap = soup.find("div", class_ = "userscore_wrap feature_userscore")
    if(user_wrap is not None):
        user_a = user_wrap.find("a", class_ = "metascore_anchor")
        user_score = user_a.find("div")
        if(user_score is not None):
            user_score = user_score.text.strip()
            if(user_score == "tbd"):
                user_score = 0
            else:
                float(user_score)
        else:
            user_score = 0
    else:
        user_score = 0

    #Getting the product summary details
    product_details = soup.find("div", class_ = "section product_details")
    side_details = product_details.find("div", class_ = "details side_details")
    summary_details = side_details.find("ul", class_ = "summary_details")

    #Getting the Developer of the game
    dev_data = summary_details.find("li", class_ = "summary_detail developer")
    if(dev_data is not None):
        developer = dev_data.find("span", class_ = "data")
        developer = developer.text.strip()
    else:
        developer = "N/A"

    #Getting the Genres of the game
    genre_set = set()
    genre_data = summary_details.find("li", class_ = "summary_detail product_genre")
    if(genre_data is not None):
        for item in genre_data.find_all("span", class_ = "data"):
            genre = item.text.strip()
            genre_set.add(genre)
        for genre in genre_set:
            db.execute("insert into genre values(?, ?);", (game_id, genre))
    else:
        genre = "N/A"
        db.execute("insert into genre values (?, ?);", (game_id, genre))

    #Getting the Rating of the game
    rating_data = summary_details.find("li", class_ = "summary_detail product_rating")
    if(rating_data is not None):
        rating = rating_data.find("span", class_ = "data")
        rating = rating.text.strip()
    else:
        rating = "N/A"

    #Getting the Cover Art of the game
    product_image = soup.find("div", class_ = "product_image large_image must_play")
    image = product_image.find("img", class_ = "product_image large_image")
    source = image['src']
    if(source is None):
        source = "N/A"
    
    db.execute("insert into game values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",(game_id, game_title, developer, publisher, rating, meta_score, user_score, date, platform, source))
    connection.commit()

#Main Code   
for i in range(0, 19054):
    page_scraper(df.iloc[i, 1], i)
    print("Page:", i, "Scraped")

connection.close()
