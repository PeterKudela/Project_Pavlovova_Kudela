
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import pycountry

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_2.lower()
available_indicators = countries.keys()

def getData(charcteristics,Country):
    url = 'http://inqstatsapi.inqubu.com?api_key=c5b5c1dd6b0f4ea5&countries='+countries[Country]+'&data=' +charcteristics+'&years=1990:2016'
    return requests.get(url).json()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.Div([
    html.Label('Select country:'),
    dcc.Dropdown(id='country',
     options=[{'label': i, 'value': i} for i in available_indicators],
     value=' '),
     html.Div(id='visit')
     ],
     style={'width': '49%', 'display': 'inline-block'}),
     dcc.Graph(id='indicator-graphic')
     ])


@app.callback(
    [Output(component_id='visit', component_property='children'),
    Output('indicator-graphic', 'figure')],
    [Input(component_id='country', component_property='value')]
)
def update_output_div(input):
    return 'TOP places to visit in {}:'.format(input)


    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import pandas as pd
    import plotly.graph_objs as go
    import pycountry
    import requests

    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_2.lower()
    available_indicators = countries.keys()

    def getData(charcteristics,Country):
        url = 'http://inqstatsapi.inqubu.com?api_key=c5b5c1dd6b0f4ea5&countries='+countries[Country]+'&data=' +charcteristics+'&years=1990:2016'
        return requests.get(url).json()


    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([

        html.Div([
        html.Label('Select country:'),
        dcc.Dropdown(id='country',
         options=[{'label': i, 'value': i} for i in available_indicators],
         value=' '),
         html.Div(id='visit')
         ],
         style={'width': '49%', 'display': 'inline-block'}),

         html.Div([
            dcc.Graph(
                id='indicator-graphic')
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})
         ])


    @app.callback(
        dash.dependencies.Output(component_id='visit', component_property='children'),
        [dash.dependencies.Input(component_id='country', component_property='value')])

    def update_output_div(input):
        return 'TOP places to visit in {}:'.format(input)

    @app.callback(
        dash.dependencies.Output(component_id='indicator-graphic', component_property='figure'),
        [dash.dependencies.Input(component_id='country', component_property='value')])

    def update_graph(country):
        data = getData('population',country)
        years = []
        popul= []
        for i in data[0]['population']:
            popul.append(int(i['data']))
            years.append(int(i['year']))
        return {
            'data': [go.Scatter(
                x=years,
                y=popul,
                text=country,
                mode='markers',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )],
            'layout': go.Layout(
                xaxis={
                    'title': 'Years'
                },
                yaxis={
                    'title': 'Population',
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
        }


    if __name__ == '__main__':
        app.run_server(debug=True)




if __name__ == '__main__':
    app.run_server(debug=True)
