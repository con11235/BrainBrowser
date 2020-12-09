# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import plotly.express as px

import base64
import datetime
import io
import csv
import pandas as pd
import numpy as np

from app import app
from datas import FS_DATA, MODULES, MESH
from utils import plot_layout,get_circos,create_3D_connectivity,create_mesh_data

app.layout = html.Div([
    # Store
    dcc.Store(id='session-fs', storage_type='session'),
    dcc.Store(id='session-obj', storage_type='session'),
    dcc.Store(id='session-con', storage_type='session'),

    # Header
    html.Header([
        html.Div([
            html.Div([
                # Logo
                html.Div([
                    html.A(html.Img(src="assets/img/logo.png", alt="MyBrain", title="Project Name"),className="scrollto",href="/")
                ],className="pull-left",id="logo"),

                # Nav
                html.Nav([
                    html.Ul([
                        html.Li(html.A("Home", href = '#intro')),
                        html.Li(html.A("About",href='#about')),
                        html.Li(html.A("Data",href='#data')),
                        html.Li(html.A("Analysis",href='#analysis')),
                        html.Li(html.A("3D Brain",href='#brain')),
                        html.Li(html.A("Table",href='#table')),
                        html.Li(html.A("Graph",href='#graph')),
                        html.Li(html.A("Connectivity",href='#connectivity')),
                    ], className="nav-menu")
                ],id="nav-menu-container")
            ],className='row')
        ],className="container"),
    ],id="header"),
    # End Header

    # Intro Section
    html.Section([
        html.Div([
            html.H1(["The Visualizer Of",html.Br(),html.Span("Brain Data")], className="mb-4 pb-0"),
            html.P("Seunghye Park, Kyung-Hee Univ.",className="mb-4 pb-0"),
            html.A("Basic Data", href="#analysis", className="about-btn scrollto"),
            html.A("Own Data", href="#data", className="about-btn scrollto"),
        ],className="intro-container", **{'data-aos':"zoom-in", 'data-aos-delay':"100"})
    ],id="intro"),
    # End Intro Section

    # Main
    html.Main([

        # About Section
        html.Section([
            html.Div([
                html.Div([
                    html.Div([
                        html.H2("About"),
                        html.P("This project is a web-based 3D visualization tool designed to effectively and interactively\
                                visualize your brain data. Each graph can be changed to the type you want (e.g. Scatter vs Box vs \
                                Violin, Circos vs. 3D). Clicking on the brain region in the 3D Brain section changes the result\
                                information below to show you the information in the clicked area. Choose Basic Data if you want\
                                to use basic data to check the results, or Own Data if you want to apply your data."),
                        html.A("Read the code on GitHub",href="https://github.com/con11235/BrainBrowser"),
                    ],className="col-lg-6"),
                    html.Div([
                        html.H3("3D Brain Surface Tool"),
                        html.P("3D visualization of the brain was implemented by referring to the Surface Viewer provided by MCIN's BrainBrowser."),
                        html.A("BrainBrowser - MCGILL CENTRE for INTEGRATIVE NEUROSCIENCE",href="https://mcin.ca/technology/visualization/brainbrowser/"),
                    ],className="col-lg-3"),
                    html.Div([
                        html.H3("Visualization Tools"),
                        html.P("All implementations of the web and plot used the Dash of Plotly."),
                        html.A("Dash Overview - Plotly",href="https://plotly.com/dash/"),
                    ],className="col-lg-3"),
                ],className="row"),
            ],className="container", **{'data-aos':"fade-up"}),
        ],id="about"),
        # End About Section

        # Data Section
        html.Section([
            html.Div([
                html.Div([
                    html.H2("Data"),
                    html.P("Get information of basic data"),
                    html.H5("Or"),
                    html.P("Upload your own data"),
                ],className="section-header"),
                html.Div([
                    html.Div([
                        dcc.Upload(html.Div([
                            html.H1(['Load ',html.Span("Structural MRI"),' Data'],className="mb-4 pb-0"),
                            html.P(['Drag and Drop or ', html.A('Select Files!')])
                            ]),
                            className="data",
                            id='upload-fsdata',
                            style={
                                'width': '100%',
                                'height': '20%',
                                'lineHeight': '30px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '10px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            # Allow multiple files to be uploaded
                            multiple=False
                        ),
                        html.P("The file extension for Structural MRI data must be .csv. The file must have a header about the vertical thickness and area information according to 66 sections of free-surfer, and data about one person in one row."),
                        html.A("Check out the exact file structure here.",href="https://github.com/con11235/BrainBrowser/blob/main/data/free_surfer_data2.csv")
                    ],className='col-lg-4'),
                    html.Div([
                        dcc.Upload(html.Div([
                            html.H1(['Load ',html.Span("Atlas"),' Data'],className="mb-4 pb-0"),
                            html.P(['Drag and Drop or ', html.A('Select Files!')])
                            ]),
                            className="data",
                            id='upload-objdata',
                            style={
                                'width': '100%',
                                'height': '20%',
                                'lineHeight': '30px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '10px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            # Allow multiple files to be uploaded
                            multiple=False
                        ),
                        html.P("The file extension for Atlas data must be .txt. The file has one number per line and must represent each integer value you want to represent on 66 free-surfer surfaces."),
                        html.A("Check out the exact file structure here.",href="https://github.com/con11235/BrainBrowser/blob/main/data/atlas_test.txt")
                    ],className='col-lg-4'),
                    html.Div([
                        dcc.Upload(html.Div([
                            html.H1(['Load ',html.Span("Brain Connectivity"), ' Data'],className="mb-4 pb-0"),
                            html.P(['Drag and Drop or ', html.A('Select Files!')])
                            ]),
                            className="data",
                            id='upload-condata',
                            style={
                                'width': '100%',
                                'height': '20%',
                                'lineHeight': '30px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '10px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            # Allow multiple files to be uploaded
                            multiple=False
                        ),
                        html.P("The file extension for Structural MRI data must be .csv.The file must have data in rows 66 and 66 without a header, which means the Brain connectivity between each section. The sequence of sections must be entered accurately."),
                        html.A("Check out the exact file structure here.",href="https://github.com/con11235/BrainBrowser/blob/main/data/connectivity_test.csv")
                    ],className='col-lg-4'),
                ], className="row"),
                html.Div([
                    dbc.Button("Upload Complete", id="upload-done"),
                ],className='btn'),
            ],className="container", **{'data-aos':"fade-up"}),
        ],id="data",className="section-with-bg"),
        # End Data Section

        # Analysis
        html.Section([
            html.Div([
                html.Div([
                    html.H2("Analysis"),
                    html.P("Show Graphs of Data"),
                    html.P("You can choose Type of Graph"),
                    html.P("The data is divided into modules."),
                ],className="section-header"),
                dcc.Dropdown(
                    id = 'analysis-type-dropdown',
                    options =  [
                        {'label' : 'Box', 'value':'B'},
                        {'label' : 'Violin', 'value':'V'}
                    ],
                    value = 'B'
                ),
                dbc.Row([
                    dbc.Col([dcc.Graph(id='graph1'),dcc.Graph(id='graph3'),dcc.Graph(id='graph5')]),
                    dbc.Col([dcc.Graph(id='graph2'),dcc.Graph(id='graph4'),dcc.Graph(id='graph6')]),
                ],className='graphs'),
            ],className="container", **{'data-aos':"fade-up"}),
        ],id="analysis"),
        # End Analysis

        # 3D Brain
        html.Section([
            html.Div([
                html.Div([
                    html.H2("3D Brain"),
                    html.P("See 3D_viewer of Brain with free-surfer"),
                ],className="section-header"),
                dcc.Graph(
                    id="brain-graph",
                    style={'height':'100vh'},
                    config={"editable": True, "scrollZoom": True},
                )
            ],className="container", **{'data-aos':"fade-up"}),
        ],id="brain",className="section-with-bg"),
        # End 3D Brain

        # Table
        html.Section([
            html.Div([
                html.Div([
                    html.H2("Table"),
                    html.P("You can get table of section you clicked"),
                    html.P("about Volumn, Thickness, and Area."),
                ],className="section-header"),
                html.Div(id='interact1-content'),
            ],className="container", **{'data-aos':"fade-up"}),
        ],id="table"),
        # End Table

        # Graph
        html.Section([
            html.Div([
                html.Div([
                    html.H2("Graph"),
                    html.P("You can get graph of section you clicked"),
                    html.P("about Volumn, Thickness, and Area."),
                ],className="section-header"),
                html.Div([
                    dcc.Dropdown(
                        id = 'graph-type-dropdown',
                        options=[
                            {'label' : 'Scatter', 'value':'S'},
                            {'label' : 'Box', 'value':'B'}
                        ],
                        value = 'S'
                    ),
                    html.Div(id='graph-content',className='graph'),
                ]),
            ],className="container", **{'data-aos':"fade-up"}),
        ],id="graph",className="section-with-bg"),
        # End Graph

        # Connectivity
        html.Section([
            html.Div([
                html.Div([
                    html.H2("Connectivity"),
                    html.P("You can get connectivity data of brain."),
                    html.P("You can choose Type of visualize"),
                ],className="section-header"),
                dcc.Dropdown(
                    id = 'connectivity-type-dropdown',
                    options=[
                        {'label' : 'Circos', 'value':'C'},
                        {'label' : '3D', 'value':'3'}
                    ],
                    value = 'C'
                ),
                html.Div(id='connectivity-content',className='graph')
            ],className="container", **{'data-aos':"fade-up"}),
        ],id="connectivity"),
        # End Connectivity

    ],id="main"),
    # End Main

    # Footer
    html.Footer([

        html.Div([
            html.Div([u"\u00A9"," Copyright ",html.Strong("TheEvent"),". All Rights Reserved"],className="copyright"),
            html.Div([
                # All the links in the footer should remain intact.
                # You can delete the links only if you purchased the pro version.
                # Licensing information: https://bootstrapmade.com/license/
                # Purchase the pro version with working PHP/AJAX contact form: https://bootstrapmade.com/buy/?theme=TheEvent
                "Designed by ", html.A("BootstrapMade",href="https://bootstrapmade.com/")
            ], className="credits")
        ],className="container")

    ],id="footer"),
    # End Footer

])

@app.callback(Output('interact1-content','children'),
    [Input("brain-graph", "clickData")],
    State('session-fs', 'data'))
def display_click_data(click_data, se_data):   # click_data : dict -> x, y, z, pointNumber, intensity
    global atlas
    if se_data != None:
        df = pd.DataFrame(se_data[0],columns = se_data[1])
    else:
        df = FS_DATA
    if click_data is None:
        return html.H1("Click any point on 3D Brain")
    else:
        x = click_data["points"][0]["x"]
        y = click_data["points"][0]["y"]
        z = click_data["points"][0]["z"]
    atlas = click_data["points"][0]["intensity"]
    atlas = list(df.columns)[57:][atlas][:-5]
    data = df[['Subject','Age','Sex','BrainSeg_Vol',atlas+'_Thck',atlas+'_Area']].copy()
    data.rename(columns = {'BrainSeg_Vol':'BrainSegment\nVolume', atlas+'_Thck':atlas+'\nThickness',atlas+'_Area':atlas+'\nArea'}, inplace = True)
    des = data.describe()[['BrainSegment\nVolume',atlas+'\nThickness',atlas+'\nArea']]
    des.reset_index(drop = False,inplace=True)
    des.rename(columns = {'index' : 'stats'})
    content = html.Div([
        dbc.Col([
            html.Div([
                html.H3("You clicked point ("+str(x)+', '+str(y)+', '+str(z)+'), and it is '+atlas),
                html.Hr(),
                dbc.Table.from_dataframe(des.iloc[1:], striped=True, bordered=True, hover=True),
                html.Hr()
            ]),
            html.Div(
                dbc.Table.from_dataframe(data, striped=True, bordered=True, hover=True),
                style={"overflow": "scroll", "height": "400px"}
            )
        ])
    ])
    return content

@app.callback(Output("graph-content","children"),
    Input("brain-graph", "clickData"),
    [
        State('graph-type-dropdown', 'value'),
        State('session-fs', 'data'),
    ]
)
def graph_to_scatter(click_data,value, se_data):
    global atlas
    if click_data is None:
        return html.H1("Click any point on 3D Brain")
    if se_data != None:
        df = pd.DataFrame(se_data[0],columns = se_data[1])
    else:
        df = FS_DATA
    atlas = click_data["points"][0]["intensity"]
    atlas = list(df.columns)[57:][atlas][:-5]
    if 'B' in value:
        main_fig = px.box(df,x="Age",y="BrainSeg_Vol",color="Sex",labels={"BrainSeg_Vol": "Volumn of BrainSegment"})
        thk_fig = px.box(df,x="Age",y=atlas+'_Thck',color="Sex",labels={atlas+'_Thck': "Thickness of "+atlas})
        area_fig = px.box(df,x="Age",y=atlas+'_Area',color="Sex",labels={atlas+'_Area': "Area of "+atlas})
    elif 'S' in value:
        main_fig = px.scatter(df,x="Age",y="BrainSeg_Vol",color="Sex",trendline="ols",labels={"BrainSeg_Vol": "Volumn of BrainSegment"})
        thk_fig = px.scatter(df,x="Age",y=atlas+'_Thck',color="Sex",trendline="ols",labels={atlas+'_Thck': "Thickness of "+atlas})
        area_fig = px.scatter(df,x="Age",y=atlas+'_Area',color="Sex",trendline="ols",labels={atlas+'_Area': "Area of "+atlas})
    main_fig.update_layout(title_text="Main Graph", title_font_size=30,paper_bgcolor='#f6f7fd',plot_bgcolor='#fff')
    thk_fig.update_layout(title_text="Thickness Graph", title_font_size=20,paper_bgcolor='#f6f7fd',plot_bgcolor='#fff')
    area_fig.update_layout(title_text="Area Graph", title_font_size=20,paper_bgcolor='#f6f7fd',plot_bgcolor='#fff')
    return [
            dcc.Graph(id='main-graph',figure=main_fig,style={
                                'width': '80%',
                                'height': '100%',
                                'textAlign': 'center',
                                'margin': '10px'
                            },),
            dcc.Graph(id='thk-graph',figure=thk_fig,style={
                                'width': '80%',
                                'height': '100%',
                                'textAlign': 'center',
                                'margin': '10px'
                            }),
            dcc.Graph(id='area-graph',figure=area_fig,style={
                                'width': '80%',
                                'height': '100%',
                                'textAlign': 'center',
                                'margin': '10px'
                            })
        ]


@app.callback(
    [
        Output("graph1","figure"),
        Output("graph2","figure"),
        Output("graph3","figure"),
        Output("graph4","figure"),
        Output("graph5","figure"),
        Output("graph6","figure"),
    ],
    [
        dash.dependencies.Input('analysis-type-dropdown', 'value'),
        Input('session-fs','data')
    ]
)
def graph_to_scatter(value, se_data):
    if se_data != None:
        df = pd.DataFrame(se_data[0],columns = se_data[1])
    else:
        df = FS_DATA
    cols = MODULES
    if 'V' in value:
        fig_1 = px.violin(df[[i+'_Thck' for i in cols[0]]+["Sex"]],color="Sex")
        fig_2 = px.violin(df[[i+'_Thck' for i in cols[1]]+["Sex"]],color="Sex")
        fig_3 = px.violin(df[[i+'_Thck' for i in cols[2]]+["Sex"]],color="Sex")
        fig_4 = px.violin(df[[i+'_Thck' for i in cols[3]]+["Sex"]],color="Sex")
        fig_5 = px.violin(df[[i+'_Thck' for i in cols[4]]+["Sex"]],color="Sex")
        fig_6 = px.violin(df[[i+'_Thck' for i in cols[5]]+["Sex"]],color="Sex")
    elif 'B' in value:
        fig_1 = px.box(df[[i+'_Thck' for i in cols[0]]+["Sex"]],color="Sex")
        fig_2 = px.box(df[[i+'_Thck' for i in cols[1]]+["Sex"]],color="Sex")
        fig_3 = px.box(df[[i+'_Thck' for i in cols[2]]+["Sex"]],color="Sex")
        fig_4 = px.box(df[[i+'_Thck' for i in cols[3]]+["Sex"]],color="Sex")
        fig_5 = px.box(df[[i+'_Thck' for i in cols[4]]+["Sex"]],color="Sex")
        fig_6 = px.box(df[[i+'_Thck' for i in cols[5]]+["Sex"]],color="Sex")
    fig_1.update_layout(title_text="Part 1", title_font_size=20,height=450,width=600)
    fig_2.update_layout(title_text="Part 2", title_font_size=20,height=450,width=600)
    fig_3.update_layout(title_text="Part 3", title_font_size=20,height=450,width=600)
    fig_4.update_layout(title_text="Part 4", title_font_size=20,height=450,width=600)
    fig_5.update_layout(title_text="Part 5", title_font_size=20,height=450,width=600)
    fig_6.update_layout(title_text="Part 6", title_font_size=20,height=450,width=600)
    return fig_1, fig_2, fig_3, fig_4, fig_5, fig_6


@app.callback(
    Output('upload-fsdata', 'children'),
    Input('upload-fsdata', 'contents'),
    State('upload-fsdata', 'filename'))
def uploaded_data(content, name):
    if content is not None:
        return [html.H1('Structural MRI file name is '),html.H1(html.Span(name))]
    return html.Div([
            html.H1(['Load ',html.Span("Structural MRI"),' Data'],className="mb-4 pb-0"),
            html.P(['Drag and Drop or ', html.A('Select Files!')])
            ])



@app.callback(Output('session-fs', 'data'),
            Input("upload-done", 'n_clicks'),
            State('upload-fsdata', 'contents'),
            State('upload-fsdata', 'filename'))
def update_output(n_clicks,content, name):
    if content is not None:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if '.csv' in name:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif '.xls' in name:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
            return [df.values.tolist(),df.columns.values.tolist()]
        except Exception as e:
            print(e)
    return None

@app.callback(
    Output('upload-objdata', 'children'),
    Input('upload-objdata', 'contents'),
    State('upload-objdata', 'filename'))
def uploaded_data(content, name):
    if content is not None:
        return [html.H1('Atlas file name is '),html.H1(html.Span(name))]
    return html.Div([
            html.H1(['Load ',html.Span("Atlas"),' Data'],className="mb-4 pb-0"),
            html.P(['Drag and Drop or ', html.A('Select Files!')])
            ])


@app.callback(Output('session-obj', 'data'),
            Output("brain-graph","figure"),
            Input("upload-done", 'n_clicks'),
            State('upload-objdata', 'contents'),
            State('upload-objdata', 'filename'))
def update_output(n_clicks,content,name):
    if content is not None:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        try:
            data = io.StringIO(decoded.decode('utf-8')).read().split('\n')
            data = [int(i) for i in data]
            return data,{'data':create_mesh_data(atlas_data=data),'layout':plot_layout}
        except Exception as e:
            print(e)
    return None,{'data':MESH,'layout':plot_layout}


@app.callback(
    Output('upload-condata', 'children'),
    Input('upload-condata', 'contents'),
    State('upload-condata', 'filename'))
def uploaded_data(content, name):
    if content is not None:
        return [html.H1('Brain Connectivity file name is '),html.H1(html.Span(name))]
    return html.Div([
            html.H1(['Load ',html.Span("Brain Connectivity"), ' Data'],className="mb-4 pb-0"),
            html.P(['Drag and Drop or ', html.A('Select Files!')])
            ])


@app.callback(Output('session-con', 'data'),
            Input("upload-done", 'n_clicks'),
            State('upload-condata', 'contents'),
            State('upload-condata', 'filename'))
def update_output(n_clicks,content,name):
    if content is not None:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if '.csv' in name:
                data = np.genfromtxt(io.StringIO(decoded.decode('utf-8')), delimiter=',') 
            return data.tolist()
        except Exception as e:
            print(e)
    return None
        


@app.callback(Output('connectivity-content','children'),
        Input("brain-graph", "clickData"),
        Input('connectivity-type-dropdown', 'value'),
        Input('session-con','data'))
def display_click_data(click_data,value,se_data):   # click_data : dict -> x, y, z, pointNumber, intensity
    if click_data is None:
        atlas=None
    else:
        atlas = click_data["points"][0]["intensity"]
    if '3' in value:
        content = dcc.Graph(
            figure= create_3D_connectivity(atlas,se_data),
            style={'height':'90vh'},
            config={"editable": True, "scrollZoom": True},
        )
        return content
    return get_circos(atlas,se_data)

if __name__ == '__main__':
    app.run_server()