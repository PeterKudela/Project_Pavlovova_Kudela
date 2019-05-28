
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import pycountry
import requests
import json



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
            'Happiness Index':'happiness_index'}
def getData(characteristic,country):
    url = 'http://inqstatsapi.inqubu.com?api_key=c5b5c1dd6b0f4ea5&countries='+countries.get(country)+'&data=' +characteristic+'&years=1990:2016'
    return requests.get(url).json()

with open('Tripadvisor.json', 'r') as f:
        datastore = json.load(f)
datastore

attractions = {}
for country in datastore:
    attractions[country['country']]=country['attractions']


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(
        children=' COUNTRY OVERVIEW'),
    html.Div([
    html.Label('Select country:'),
    dcc.Dropdown(id='country',
     options=[{'label': c, 'value': c} for c in countries.keys()],
     value='Czechia'),
     html.H1(children='  '),
     html.Div(id='capital'),
     html.H1(children='  '),
     html.Div(id='visit'),
     html.Table([
        html.Tr([html.Td(['1']), html.Td(id='1')]),
        html.Tr([html.Td(['2']), html.Td(id='2')]),
        html.Tr([html.Td(['3']), html.Td(id='3')]),
        html.Tr([html.Td(['4']), html.Td(id='4')]),
        html.Tr([html.Td(['5']), html.Td(id='5')]),
    ])],style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),
     html.Div([
        html.Label('Select the charcteristic of interest:'),
        dcc.Dropdown(id='characteristic',
         options=[{'label': ch, 'value': characteristics_dict.get(ch)} for ch in characteristics_dict.keys()],
         value='population'),
        dcc.Graph(
            id='indicator-graphic')
    ],style={'width': '49%', 'float': 'left','display': 'inline-block'}),
     ])

@app.callback(
    dash.dependencies.Output(component_id='capital', component_property='children'),
    [dash.dependencies.Input(component_id='country', component_property='value')])

def capital(country):
    return 'Capital: {}'.format(getData('capital_name',country)[0]['capital_name'])

@app.callback(
    dash.dependencies.Output(component_id='visit', component_property='children'),
    [dash.dependencies.Input(component_id='country', component_property='value')])

def update_output_div(country):
    if attractions[country][0:6] != []:
        no_data =''
    else:
        no_data = 'No DATA AVAILABLE :('
    return 'TOP places to visit in {}: {}'.format(country, no_data)


@app.callback(
    [Output('1', 'children'),
     Output('2', 'children'),
     Output('3', 'children'),
     Output('4', 'children'),
     Output('5', 'children')],
    [Input('country', 'value')])
def top_places_to_visit(country):
    if attractions[country][0:6] != []:
        return attractions[country][0], attractions[country][1], attractions[country][2],attractions[country][3], attractions[country][4]
    else:
        return 'NA','NA','NA','NA','NA'

@app.callback(
    dash.dependencies.Output(component_id='indicator-graphic', component_property='figure'),
    [dash.dependencies.Input(component_id='country', component_property='value'),
     dash.dependencies.Input(component_id='characteristic', component_property='value')])

def update_graph(country,characteristic):
    data = getData(characteristic,country)
    years=[]
    char=[]
    if (data != {'type': 'error', 'msg': 'Invalid data argument.'}
       and data[0][characteristic] !=[]):
        for i in data[0][characteristic]:
            years.append(i['year'])
            char.append(i['data'])
        title_graph = ' '
    else:
        years = list(range(1990,2017))
        popul = [0]*27
        title_graph = 'DATA NOT AVAILABLE'
    return {
        'data': [go.Scatter(
                x=years,
                y=char,
                mode='lines+markers',
                marker={
                    'size': 10,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'blue'}
                    }
                    )],
                'layout': go.Layout(
                    xaxis={
                        'title': 'Years'
                    },
                    yaxis={
                        'title': list(characteristics_dict.keys())[list(characteristics_dict.values()).index(characteristic)],
                        },
                    title = title_graph,
                    margin={'l': 60, 'b': 30, 't': 30, 'r': 30},
                    hovermode='closest'
                        )
                        }


if __name__ == '__main__':
    app.run_server(debug=True)
