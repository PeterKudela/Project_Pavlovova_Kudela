import requests
from bs4 import BeautifulSoup
import pandas as pd
import pycountry

def getSoup(link):
    r = requests.get(link)
    r.encoding = 'UTF-8'

    return BeautifulSoup(r.text,'lxml')

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_2.lower()
countries_names = [countries.keys()]

links_google= ["https://www.google.com/search?q=tripadvisor+15+best+things+to+do+in+" + x for x in countries.keys()]

links_tripadvisor=[]
for i in links_google:
    soup = getSoup(i)
    h3=soup.find('h3', {'class':"r"})
    a=h3.contents[0]
    url=a.get('href')
    url=url.partition("Attractions")[2].partition(".html")[0]
    ta = 'http://tripadvisor.com/Attractions'
    adress= ta+url
    links_tripadvisor.append(adress)
