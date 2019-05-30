
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
            'Happiness Index':'happiness_index','Public Expenditure on health ( % of the GDP)':'health_expenditure',
            'The average number a person will live':'life_expectancy','The amount of expenditures dedicated for tourism ( % of GDP)':'tourism_expenditure'}
def getData(characteristic,country):
    url = 'http://inqstatsapi.inqubu.com?api_key=c5b5c1dd6b0f4ea5&countries='+countries.get(country)+'&data=' +characteristic+'&years=1990:2016'
    return requests.get(url).json()

def getDataWorld(charcteristics,year):
    url = 'http://inqstatsapi.inqubu.com?api_key=c5b5c1dd6b0f4ea5&cmd=getWorldData&data=' +charcteristics+'&year='+year
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
        html.H1(
            children=' COUNTRY OVERVIEW',
            style={'textAlign': "center", "padding-bottom": "30", 'color':'lightblue'}),
            dcc.Dropdown(id='country',
             options=[{'label': c, 'value': c} for c in countries.keys()],
             value='Czechia',style = { 'textAlign':'center'})]),
     html.H1(children='  '),
     html.Div(id='capital',style={'textAlign':'center'}),
     html.H1(children='  '),
     html.Div([
        html.Div([
            html.Div(id='visit',style={'background':'lightblue','textAlign':'center'}),
                html.Table([
                html.Tr([html.Td(['1']), html.Td(id='1')]),
                html.Tr([html.Td(['2']), html.Td(id='2')]),
                html.Tr([html.Td(['3']), html.Td(id='3')]),
                html.Tr([html.Td(['4']), html.Td(id='4')]),
                html.Tr([html.Td(['5']), html.Td(id='5')]),
                html.Tr([html.Td(['6']), html.Td(id='6')]),
                html.Tr([html.Td(['7']), html.Td(id='7')]),
                html.Tr([html.Td(['8']), html.Td(id='8')]),
                html.Tr([html.Td(['9']), html.Td(id='9')]),
                html.Tr([html.Td(['10']), html.Td(id='10')])])],style={'width': '49%', 'display': 'inline-block',}),
        html.Div([
            html.Label(children='Location:',style={'background':'lightblue','textAlign':'center'}),
            dcc.Graph(id='map_single')],
                style={'width': '49%', 'display': 'inline-block'})]),
    html.Div([
        html.Div([
            html.Label('Select the characteristic of interest:',style={'background':'lightblue','textAlign':'center'})]),
        html.Div([
            dcc.Dropdown(id='characteristic',
         options=[{'label': ch, 'value': characteristics_dict.get(ch)} for ch in characteristics_dict.keys()],
         value='population')],style={'textAlign':'center'})]),
    html.Div([
            html.Div([
                dcc.Graph(id='indicator-graphic')],style={'width': '49%','float':'left'}),
            html.Div([
                html.Div(id = 'world-char'),
                dcc.Graph(id="my-graph")],style={'width': '49%','float':'right'})])
    ])

@app.callback(
    dash.dependencies.Output("world-char", "children"),
    [dash.dependencies.Input("characteristic", "value")]
)

def world_map_header(char):
    return '{} around the world'.format(list(characteristics_dict.keys())[list(characteristics_dict.values()).index(char)])
@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("characteristic", "value")]
)
def update_figure(selected):
    df=pd.read_json(json.dumps(getDataWorld(selected,'2014')))
    trace = go.Choropleth(locations=df['countryName'],z=df[selected],text = df['countryName'],
                            autocolorscale=False, locationmode = 'country names',
                            colorscale = "YlGnBu", marker = {'line':{'color':'rgb(180,180,180)','width':0.5}},
                          colorbar={"thickness": 10,"len": 0.3,"x": 0.1,"y": 0.2,
                                    'title': {"text": selected, "side": "bottom"}})
    return {"data": [trace],
            "layout": go.Layout(height=500,margin=go.layout.Margin(l=0,r=0,b=0,t=0,pad=4),geo={'showframe': False,'showcoastlines': True,'projection': {'type': "miller"}})}

@app.callback(
    dash.dependencies.Output(component_id='capital', component_property='children'),
    [dash.dependencies.Input(component_id='country', component_property='value')])

def capital(country):
    return 'Capital: {}'.format(getData('capital_name',country)[0]['capital_name'])

@app.callback(
    dash.dependencies.Output(component_id='visit', component_property='children'),
    [dash.dependencies.Input(component_id='country', component_property='value')])

def update_output_div(country):
    if attractions[country][0:10] != []:
        no_data =''
    else:
        no_data = 'No DATA AVAILABLE :('
    return 'TOP places to visit in {}: {}'.format(country, no_data)


@app.callback(
    [Output('1', 'children'),
     Output('2', 'children'),
     Output('3', 'children'),
     Output('4', 'children'),
     Output('5', 'children'),
     Output('6', 'children'),
     Output('7', 'children'),
     Output('8', 'children'),
     Output('9', 'children'),
     Output('10', 'children'),],
    [Input('country', 'value')])
def top_places_to_visit(country):
    if attractions[country][0:10] != []:
        return attractions[country][0], attractions[country][1], attractions[country][2],attractions[country][3], attractions[country][4],attractions[country][5],attractions[country][6],attractions[country][7],attractions[country][8],attractions[country][9]
    else:
        return 'NA','NA','NA','NA','NA','NA','NA','NA','NA','NA'
@app.callback(
    dash.dependencies.Output("map_single", "figure"),
    [dash.dependencies.Input("country", "value")]
)
def update_figure2(country):

    trace2 = go.Choropleth(locations= [country],z=[1],text = country,
                            autocolorscale=True, locationmode = 'country names',showscale= False)
    return {"data": [trace2],
            "layout": go.Layout(height=500,margin=go.layout.Margin(l=0,r=0,b=0,t=0,pad=4),geo={'showframe': False,'showcountries':True,'showcoastlines': True,'projection': {'type': "miller"}})}
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
                    'size': 5,
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
