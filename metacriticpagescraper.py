#MeteCritic URL Retriever
import requests, csv, pandas as pd, pprint, time
from bs4 import BeautifulSoup
import lxml, html5lib

url_dict = {'url':[]} # Data Structure

def webpage(pageNum, year): #function that navigates the Metacritic SRP(Search Results Pages) based on the page number and the year
    url = 'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected='+ str(year) +'&distribution=&sort=desc&view=condensed&page='+ str(pageNum)
    userAgent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=userAgent)
    return response

def numberPages(response): # Helper Function that determines how many pages are in a SRP to know how many times to run scrapper function
    soup = BeautifulSoup(response.text, 'html.parser')
    pages = soup.find_all('li', {"class":"page last_page"})
    pagesCleaned = pages[0].find('a', {"class":"page_num"})
    return (pagesCleaned.text)

def scrapper(num_loops, content):
    tblnum = 0
    while tblnum < num_loops:
        #getting game url
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for a in td[1].find_all('a', {"class":"title"} ,href=True):
                url_dict['url'].append(a['href'])
        tblnum += 1

def pages(lastPageNum, year): #Function that returns the html(code) and initiates the URL Retriever
    currentPage = 0
    while currentPage < int(lastPageNum):
        url = url = 'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected='+ str(year) +'&distribution=&sort=desc&view=condensed&page=' + str(currentPage)
        userAgent = {'User-agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=userAgent)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find_all('table')
        num_loops = len(content)
        scrapper(num_loops, content)
        currentPage += 1
        print(currentPage)
        time.sleep(6)

#Main code
years = list(range(1995, 1998))
for year in years:
    if(year < 2000):
        pages(1, year)
        time.sleep(5)
        print(year)
    else:
        numPage = (numberPages(webpage(0, year)))
        pages(int(numPage), year)
        time.sleep(5)
        print(year)
url_data = (pd.DataFrame.from_dict(url_dict))
url_data.to_csv(r"..\MetacriticWebscraperandDB\gameurls.csv")

