import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import json, requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def getDataWorld(charcteristics,year):
    url = 'http://inqstatsapi.inqubu.com?api_key=c5b5c1dd6b0f4ea5&cmd=getWorldData&data=' +charcteristics+'&year='+year
    return requests.get(url).json()


if 'DYNO' in os.environ:
    app_name = os.environ['DASH_APP_NAME']
else:
    app_name = 'dash-choroplethplot'

app.layout = html.Div([html.Div([html.H1("Demographic Data by Country")],
                                style={'textAlign': "center", "padding-bottom": "30"}),
                       html.Div([html.Span("Metric to display : ", className="six columns",
                                           style={"text-align": "right", "width": "40%", "padding-top": 10}),
                                 dcc.Dropdown(id="selected", value='population',
                                              options=[{'label': "Population ", 'value': 'population'},
                                              {'label': 'Happiness Index', 'value':'happiness_index'},
                                              {'label': 'mnam', 'value': 'mnam'}],
                                              style={"display": "block", "margin-left": "auto", "margin-right": "auto",
                                                     "width": "70%"},
                                              className="six columns")], className="row"),
                       dcc.Graph(id="my-graph")
                       ], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("selected", "value")]
)
def update_figure(selected):
    df=pd.read_json(json.dumps(getDataWorld(selected,'2016')))
    iso=[]
    for country in df['countryCode']:
        try:
            iso.append(pycountry.countries.get(alpha_2=country.upper()).alpha_3)
        except:
            iso.append(' ')
            pass
    df = pd.concat([df,pd.Series(iso)],axis = 1)
    df.columns = ['countryCode', 'countryName', selected, 'year','iso_alpha']
    trace = go.Choropleth(locations=df['countryName'],z=df[selected],text = df['countryName'],
                            autocolorscale=False, locationmode = 'country names',
                            colorscale = "YlGnBu", marker = {'line':{'color':'rgb(180,180,180)','width':0.5}},
                          colorbar={"thickness": 10,"len": 0.3,"x": 0.9,"y": 0.7,
                                    'title': {"text": selected, "side": "bottom"}})
    return {"data": [trace],
            "layout": go.Layout(title= selected,height=800,geo={'showframe': False,'showcoastlines': True,'projection': {'type': "miller"}})}
if __name__ == '__main__':
    app.run_server(debug=True)
