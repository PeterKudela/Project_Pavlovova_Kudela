import pandas as pd
import plotly.graph_objs as go
import pycountry
import requests
import json
import numpy as np

'''
Creating dictionary with country name and its ISO 3166-1 Alpha-2 code for each country (ex. Czechia:cz).

'''
countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_2.lower()

characteristics_dict = {'BigMac Index': 'bigmac_index','The average number of birth per year per 1,000 population': 'birth_rate',
             'CO2 emissions (in metric tons per person per year)':'co2_emissions', 'Corruption index':'corruption_index',
            'Density':'density', 'Death rate': 'death_rate',
            'The total amount of government borrowings (unit: USD)':'debts',
            'Population':'population', 'The amount of government borrowings per person (unit: USD)':'debts_capita',
            'The percentage of government borrowings in relation to the GDP':'debts_percent',
            'Public expenditure on education (in % of the GDP for a country)':'education_expenditure',
            'The percentage of the land area covered by a forest for a country':'forest_area_percent',
            'Gross Domestic Product per person for a country (unit: USD)':'gdp_capita',
            'Happiness Index':'happiness_index','Public Expenditure on health ( % of the GDP)':'health_expenditure',
            'Life expectanty (years)':'life_expectancy','The amount of expenditures dedicated for tourism ( % of GDP)':'tourism_expenditure'}
def getData(characteristic,country):
    url = 'http://inqstatsapi.inqubu.com?api_key=05305ba459195d25&countries='+countries.get(country)+'&data=' +characteristic+'&years=1990:2016'
    return requests.get(url).json()

def getDataWorld(charcteristics,year):
    url = 'http://inqstatsapi.inqubu.com?api_key=05305ba459195d25&cmd=getWorldData&data=' +charcteristics+'&year='+year
    return requests.get(url).json()

with open('Tripadvisor.json', 'r') as f:
        datastore = json.load(f)
datastore

attractions = {}
for country in datastore:
    attractions[country['country']]=country['attractions']
def top_places_to_visit(country):
    if attractions[country][0:10] != []:
        return attractions[country][0], attractions[country][1], attractions[country][2],attractions[country][3], attractions[country][4],attractions[country][5],attractions[country][6],attractions[country][7],attractions[country][8],attractions[country][9]
    else:
        return 'NA','NA','NA','NA','NA','NA','NA','NA','NA','NA'

def location_map_function(country):
    trace2 = go.Choropleth(locations= [country],z=[1],text = country,
                            autocolorscale=True, locationmode = 'country names',showscale= False)
    return {"data": [trace2],
            "layout": go.Layout(height=500,
            margin=go.layout.Margin(l=0,r=0,b=0,t=0,pad=4),
            geo={'showframe': False,'showcountries':True,'showcoastlines': True,'projection': {'type': "miller"}})}

def scatter(country,characteristic):
    data = getData(characteristic,country)
    years=[]
    char=[]
    if (data != {'type': 'error', 'msg': 'Invalid data argument.'}
       and data[0][characteristic] !=[]):
        for i in data[0][characteristic]:
            years.append(i['year'])
            char.append(i['data'])
        title_graph =' '
    else:
        years = list(range(1990,2017))
        popul = [0]*27
        title_graph = 'DATA NOT AVAILABLE'
    return {
        'data': [go.Scatter(
                x=years,
                y=char,
                mode='lines+markers',
                marker={'size': 5,'opacity': 0.5,'line': {'width': 0.5, 'color': 'blue'}})],
        'layout': go.Layout(
                xaxis={'title': 'Years'},
                yaxis={'title': list(characteristics_dict.keys())[list(characteristics_dict.values()).index(characteristic)],},
                title = title_graph,
                margin={'l': 60, 'b': 30, 't': 30, 'r': 30},
                hovermode='closest')}

def world_map(characteristic,year):
    df=pd.read_json(json.dumps(getDataWorld(characteristic,str(year))))
    if len(df) != 0 :
        return {"data":[go.Choropleth(locations=df['countryName'],z=df[characteristic],text = df['countryName'],
                            autocolorscale=False, locationmode = 'country names',
                            colorscale = "YlGnBu", marker = {'line':{'color':'rgb(180,180,180)','width':0.5}},
                            colorbar={"thickness": 10,"len": 0.3,"x": 0.1,"y": 0.3,
                                    'title': {"text": 'White = NA', "side": "bottom"}})],
                "layout":go.Layout(height=500,
                        margin=go.layout.Margin(l=0,r=0,b=0,t=0,pad=4),
                        geo={'showframe': False,'showcountries':True,'showcoastlines': True,'projection': {'type': "miller"}})}
    else:
        return {"data":[go.Choropleth(locations=list(countries.keys()),z=np.zeros(len(list(countries.keys()))),
                            autocolorscale=True, locationmode = 'country names',
                            colorbar={"thickness": 0.1,"len": 0.3,"x": 0.1,"y": 0.2,
                                    'title': {"text": characteristic, "side": "bottom"}})],
                "layout":go.Layout(height=500,
                        title = go.layout.Title(text = 'NO DATA. TRY DIFFERENT YEAR'),
                        margin=go.layout.Margin(l=0,r=0,b=0,t=30,pad=4),
                        geo={'showframe': False,'showcoastlines': True,'showcountries':True,'projection': {'type': "miller"}})}
