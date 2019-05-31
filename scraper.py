'''
    Web scraper that gets TOP things to visit in every country
    based on Tripadvisor rating. We get the tripadvisor websides
    special tripadvisor country codes are needed. As we did not find
    any list of them, we went around using google. The scraper first
    googles top places to visit in country x - gets the corresponding
    link and then scrapes the corresponding page.

'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pycountry
import json


def getSoup(link):
    '''
        Returns a BeautifulSoup output based on provided link
    '''
    r = requests.get(link)
    r.encoding = 'UTF-8'
    return BeautifulSoup(r.text,'lxml')


'''
Creating dictionary with country name and its ISO 3166-1 Alpha-2 code for
each country (ex. {'Czechia':'cz'}).

'''
countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_2.lower()

def getTripAdvisorLink(country):
    '''
        Returns an Tripadvisor "Best things to do" link (if available) for specific country.
        Google is used as it is able to obtain specific code needed in Tripadvisor link which returns a country
        Example: g274684 for Czech Republic
    '''
    soup = getSoup('https://www.google.com/search?q=tripadvisor+best+things+to+do+in+'+str(country))
    ta = 'http://tripadvisor.com/Attractions'
    i = 0
    length = len(soup.findAll('a',href=True))
    while True:
        url=soup.findAll('a',href=True)[i].get('href').partition("Attractions")[2].partition(".html")[0]
        i+=1
        adress = ta+url
        if adress !=  ta:
            return adress
            break
        if i == length :
            break
def getTripAdvisorAttractions(link):
    '''
        Returns a list of traveller favourites attractions (at the bottom of each page) for each Tripadvisor
        link provided.
    '''
    if link is not None:
        soup = getSoup(link)
        divs = soup.findAll('div', {'class':'listing_title'})
        text_chunks = {div.contents[1] for div in divs}
        attraction_titles=[title.contents[0] for title in text_chunks]
        return attraction_titles

'''
    Returns a list of dictionatries.
    Each dictionary contains country name,tripadvisor "best things to do" link and a list of "best things to do"
'''
data = [{'country': country, 'link': getTripAdvisorLink(country),'attractions': getTripAdvisorAttractions(getTripAdvisorLink(country))} for country in countries.keys()]

'''
    Creates and saves json file from the data
'''
import json
json = json.dumps(data)
f = open("Tripadvisor.json","w")
f.write(json)
f.close()
