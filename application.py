'''
    In this file the 'application is defined'
    Meaning the layout, its inputs and outputs.
    To run the app, just run $ python application.py
    in your terminal and then open http://127.0.0.1:8050/
    in your browser.

    Functions and defined list of inputs(such as
    list of countries and characteristics) are defined
    in the file input_and_functions.
    The code depends on the way how the inputs
    are defined (e.g. countries as dict {'country':'code'}).

'''
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from inputs_and_functions import *
'''
    Defining the layout of the page (html).
'''
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1( #title
            children=' COUNTRY OVERVIEW',
            style={'textAlign': "center", "padding-bottom": "30", 'color':'lightblue'}),
        html.Label(children = 'SELECT COUNTRY:',
            style={'textAlign': "center", 'color':'lightgrey'}),#label for dropdown list of countries
        dcc.Dropdown(id='country', #dropdown list of countries, Czechia choosen as a default
             options=[{'label': c, 'value': c} for c in countries.keys()],
             value='Czechia',style = { 'textAlign':'center'})]),
     html.Div(id='capital',style={'textAlign':'center'}), #capital city based on selected country
     html.H1(children='  '), # empty line
     html.Div([
        html.Div([
            html.Div(id='visit',style={'background':'lightblue','textAlign':'center'}), # title of top places to visit
                html.Table([ #table of top places to visit
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
            html.Label(children='Location:', #title of map of location
                style={'background':'lightblue','textAlign':'center'}),
            dcc.Graph(id='map_single')], #map of location
                style={'width': '49%', 'display': 'inline-block'})]),
    html.Div([
        html.Div([
            html.Label('Select the characteristic of interest:',
                style={'background':'lightblue','textAlign':'center'})]),
        html.Div([
            dcc.Dropdown(id='characteristic', #dropdown list of possible characteristics
         options=[{'label': ch, 'value': characteristics_dict.get(ch)} for ch in characteristics_dict.keys()],
         value='population')],style={'textAlign':'center'})]),
    html.Div([
            html.Div([
                html.Div(id = 'scatter-title', #title of the scatter plot
                    style = {'textAlign':'center','color':'grey'}),
                dcc.Graph(id='indicator-graphic')], #scatter plot for the selected variable
                style={'width': '49%','float':'left'}),
            html.Div([
                html.Div(id = 'world-char',  #title for world map of the selected variable
                    style = {'textAlign':'center','color':'grey'}),
                dcc.Graph(id="my-graph"), #world map of the selected variable
                dcc.Slider(id = 'year', #time line where a year for the wolrd map can be selected
                           min=1990,
                           max=2016,
                           value=2016,
                           marks={i: {'label': str(i)} for i in range(1990,2017)},
                               included=False)],
                style={'width': '49%','float':'right'})])
])

'''
    Connectiong the elements, e.i. the inputs
    provided by user with the outputs.
'''
@app.callback(
    dash.dependencies.Output(component_id='capital', component_property='children'),
    [dash.dependencies.Input(component_id='country', component_property='value')])
# returns the capital of a country given country
def capital(country):
    return 'Capital: {}'.format(getData('capital_name',country)[0]['capital_name'])

@app.callback(
    dash.dependencies.Output(component_id='visit', component_property='children'),
    [dash.dependencies.Input(component_id='country', component_property='value')])
# prints title to the a table of top 10 attraction to visit if data available
def update_output_div(country):
    if attractions[country][0:10] != []: #checking that data are available
        no_data =''
    else: # if data not available
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
# prints the table of top 10 places to visit
def write_top_places_to_visit(country):
    return top_places_to_visit(country)

@app.callback(
    dash.dependencies.Output("map_single", "figure"),
    [dash.dependencies.Input("country", "value")]
)
#draws a world map where the given country is highlighted
def draw_location(country):
    return location_map_function(country)

@app.callback(
    dash.dependencies.Output("scatter-title", "children"),
    [dash.dependencies.Input("characteristic", "value"),
    dash.dependencies.Input("country", "value")]
)
# title for the plot below
def scatter_header(char,country):
    return '{} IN {}'.format(list(characteristics_dict.keys())[list(characteristics_dict.values()).index(char)].upper(), country.upper())

@app.callback(
    dash.dependencies.Output(component_id='indicator-graphic', component_property='figure'),
    [dash.dependencies.Input(component_id='country', component_property='value'),
     dash.dependencies.Input(component_id='characteristic', component_property='value')])
# given country and some characteristic from defined list draws the development between 1990 and 2016
def draw_scatter(country, characteristic):
    return scatter(country,characteristic)

@app.callback(
    dash.dependencies.Output("world-char", "children"),
    [dash.dependencies.Input("characteristic", "value")]
)
#title for world map of a given characteristic
def world_map_header(char):
    return '{} AROUND THE WORLD'.format(list(characteristics_dict.keys())[list(characteristics_dict.values()).index(char)].upper())

@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("characteristic", "value"),
    dash.dependencies.Input("year", "value")]
)
#for given coountry and year returns world map
def draw_world_map(characteristic,year):
    return world_map(characteristic,year)

if __name__ == '__main__':
    app.run_server(debug=True)
