from pygam import LinearGAM, s

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,title = 'Addition',external_stylesheets=[dbc.themes.BOOTSTRAP])

FS_DATA = pd.read_csv('fsData.csv')
FS_DATA["Sex"] = FS_DATA["Sex"].apply(lambda x: ["","M","F"][x])


def get_fig(sex,value,spl,title):
    if sex == 'T':
        data = FS_DATA
        color = 'rgba(123,0,123,0.2)'
        lncolor = 'rgb(123,50,123)'
    elif sex == 'F':
        data = FS_DATA[FS_DATA['Sex']=='F']
        color = 'rgba(255,0,0,0.1)'
        lncolor = 'rgb(255,100,0)'
    else:
        data = FS_DATA[FS_DATA['Sex']=='M']
        color = 'rgba(0,0,255,0.1)'
        lncolor = 'rgb(0,100,255)'
    x = data.Age.array
    y = data[value].array

    gam = LinearGAM(s(0,n_splines=spl)).fit(x, y)
    
    fig = go.Figure()
    
    for i, term in enumerate(gam.terms):
        if term.isintercept:
            continue

        XX = gam.generate_X_grid(term=i)
        pdep, confi = gam.partial_dependence(term=i, X=XX, width=0.95)

        fig.add_traces(go.Scatter(
            x=XX[:, term.feature], y=confi.T[1],
            name='UPR', line=dict(dash='dash',color = lncolor),
            hovertemplate="Age: %{x} <br>Volume: %{y}"
        ))

        fig.add_traces(go.Scatter(
            x=XX[:, term.feature], y=pdep,
            name='Mean', line=dict(color='black', width=3),
            fill='tonexty', 
            fillcolor=color,
            hovertemplate="Age: %{x} <br>Volume: %{y}"
        ))

        fig.add_traces(go.Scatter(
            x=XX[:, term.feature], y=confi.T[0],
            name='LWR', line=dict(dash='dash',color = lncolor),
            fill='tonexty', 
            fillcolor=color,
            hovertemplate="Age: %{x} <br>Volume: %{y}"
        ))
    
    if sex == 'B':
        data = FS_DATA[FS_DATA['Sex']=='F']
        x = data.Age.array
        y = data[value].array
        gam = LinearGAM(s(0,n_splines=spl)).fit(x, y)
        color = 'rgba(255,0,0,0.1)'
        lncolor = 'rgb(255,100,0)'
        for i, term in enumerate(gam.terms):
            if term.isintercept:
                continue

            XX = gam.generate_X_grid(term=i)
            pdep, confi = gam.partial_dependence(term=i, X=XX, width=0.95)

            fig.add_traces(go.Scatter(
                x=XX[:, term.feature], y=confi.T[1],
                name='UPR', line=dict(dash='dash',color = lncolor),
                hovertemplate="Age: %{x} <br>Volume: %{y}",
                opacity=0.1,
            ))

            fig.add_traces(go.Scatter(
                x=XX[:, term.feature], y=pdep,
                name='Mean', line=dict(color='black', width=3),
                fill='tonexty', 
                fillcolor=color,
                hovertemplate="Age: %{x} <br>Volume: %{y}"
            ))

            fig.add_traces(go.Scatter(
                x=XX[:, term.feature], y=confi.T[0],
                name='LWR', line=dict(dash='dash',color = lncolor),
                fill='tonexty', 
                fillcolor=color,
                hovertemplate="Age: %{x} <br>Volume: %{y}"
            ))


    fig.update_layout(
        xaxis_title="Age",
        yaxis_title=value[:-4],
        title=title,
        width=600, height=400,
        #color_discrete_map={ # replaces default color mapping by value
        #        "Male": "RebeccaPurple", "Female": "MediumPurple"
        #    },
        #fig.add_annotation( # add a text callout with arrow
        #text="below target!", x="Fri", y=400, arrowhead=1, showarrow=True
        #)
        template="simple_white"
    )

    return fig

app.layout = dbc.Container([
        html.H1("Volume of Free-Surfer Atlas"),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.FormGroup([
                        dbc.Label("Selected ROI"),
                        dcc.Dropdown(
                            id = 'roi-dropdown',
                            options=[{'label':i[:-4], 'value':i} for i in FS_DATA.columns[6:23]],
                            value='BrainSeg_Vol'
                        ),
                    ]),
                    dbc.FormGroup([
                        dbc.Label("Selected Sex"),
                        dcc.RadioItems(
                            options=[
                                {'label': 'Total', 'value': 'T'},
                                {'label': 'Both', 'value': 'B'},
                                {'label': 'Male', 'value': 'M'},
                                {'label': 'Female', 'value': 'F'}
                            ],
                            value='T',
                            id = 'sex-radio'
                        )  
                    ]),
                    dbc.FormGroup([
                        dbc.Label("Selected Spline"),
                        dcc.Slider(
                            id='spl-slider',
                            min=4,
                            max=20,
                            step=1,
                            value=10,
                        ),    
                    ]),
                    
                ],body=True,)
            ],md=4),
            dbc.Col([
                dcc.Graph(id = 'curve-graph')
            ],md=8)
        ])#,align="center",)
    ],fluid=True,)

@app.callback(
    dash.dependencies.Output('curve-graph', 'figure'),
    [dash.dependencies.Input('roi-dropdown', 'value'),
    dash.dependencies.Input('sex-radio', 'value'),
    dash.dependencies.Input('spl-slider', 'value')])
def update_output(value, sex,spl):
    fig=get_fig(sex,value, spl,"graph of GAM")
    return fig

if __name__ == '__main__':
    app.run_server(debug = True)
