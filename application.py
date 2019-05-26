
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
available_indicators = countries.keys()

def getData(charcteristics,country):
    url = 'http://inqstatsapi.inqubu.com?api_key=c5b5c1dd6b0f4ea5&countries='+countries.get(country)+'&data=' +charcteristics+'&years=1990:2016'
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

    html.Div([
    html.Label('Select country:'),
    dcc.Dropdown(id='country',
     options=[{'label': i, 'value': i} for i in available_indicators],
     value='Czechia'),
     html.Div(id='visit')
     ],
     style={'width': '49%', 'display': 'inline-block'}),

     html.Div([
        dcc.Graph(
            id='indicator-graphic')
    ], style={'width': '49%'})
     ])


@app.callback(
    dash.dependencies.Output(component_id='visit', component_property='children'),
    [dash.dependencies.Input(component_id='country', component_property='value')])

def update_output_div(input):
    if attractions[input][0:11] is not None:
        to_visit =attractions[input][0:11]
    else:
        to_visit = 'No data available. :('
    return 'TOP places to visit in {}: {}'.format(input,to_visit)

@app.callback(
    dash.dependencies.Output(component_id='indicator-graphic', component_property='figure'),
    [dash.dependencies.Input(component_id='country', component_property='value')])

def update_graph(country):
    data = getData('population',country)
    years=[]
    popul= []
    if data != {'type': 'error', 'msg': 'Invalid data argument.'}:
        for i in data[0]['population']:
            years.append(int(i['year']))
            popul.append(int(i['data']))
        title_graph = "Population"
    else:
        years = list(range(1990,2017))
        popul = [0]*27
        title_graph = 'Population - DATA NOT AVAILABLE'
    return {
        'data': [go.Scatter(
                x=years,
                y=popul,
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
                        'title': 'Population',
                        },
                    title = title_graph,
                    margin={'l': 60, 'b': 30, 't': 30, 'r': 30},
                    hovermode='closest'
                        )
                        }


if __name__ == '__main__':
    app.run_server(debug=True)