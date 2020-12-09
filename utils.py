import dash
import dash_bio
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pathlib
import numpy as np
import pandas as pd
from scipy import io
import copy
import csv

excel_file = pd.read_excel('data/Hagmann_66regions.xlsx')

axis_template = {
    "showbackground": True,
    "backgroundcolor": "#f6f7fd",
    "gridcolor": "rgb(14, 14, 14)",
    "zerolinecolor": "rgb(14,14,14)",
}

plot_layout = {
    "title": "",
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    "font": {"size": 12, "color": "black"},
    "showlegend": False,
    "plot_bgcolor": "#f6f7fd",
    "paper_bgcolor": "#f6f7fd",
    "scene": {
        "xaxis": axis_template,
        "yaxis": axis_template,
        "zaxis": axis_template,
        "aspectratio": {"x": 1, "y": 1.2, "z": 1},
        "camera": {"eye": {"x": 1.25, "y": 1.25, "z": 1.25}},
        "annotations": [],
    },
}

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()

default_colorscale = [
    [0, "rgb(181,126,237)"],
    [0.25, "rgb(141,131,247)"],
    [0.5, "rgb(130,160,224)"],
    [0.75, "rgb(131,214,247)"],
    [1, "rgb(130,240,228)"],
]

Transparent_colorscale = [
    [0, "rgb(220,220,220)"],
    [1, "rgb(220,220,220)"],
]


def read_mniobj(file):
    """
    Parses an obj file.
    
    :params file: file name in data folder
    :returns: a tuple
    """

    def triangulate_polygons(list_vertex_indices):
        for k in range(0, len(list_vertex_indices), 3):
            yield list_vertex_indices[k : k + 3]

    with open(DATA_PATH.joinpath(file)) as fp:
        num_vertices = 0
        matrix_vertices = []
        k = 0
        list_indices = []

        for i, line in enumerate(fp):
            if i == 0:
                num_vertices = int(line.split()[6])
                matrix_vertices = np.zeros([num_vertices, 3])
            elif i <= num_vertices:
                matrix_vertices[i - 1] = list(map(float, line.split()))
            elif i > 2 * num_vertices + 5:
                if not line.strip():
                    k = 1
                elif k == 1:
                    list_indices.extend(line.split())

    list_indices = [int(i) for i in list_indices]
    faces = np.array(list(triangulate_polygons(list_indices)))
    return matrix_vertices, faces


def plotly_triangular_mesh(
    vertices,
    faces,
    intensities=None,
    colorscale="Viridis",
    flatshading=False,
    showscale=False,
    opacity = 1
):

    x, y, z = vertices.T
    I, J, K = faces.T

    if intensities is None:
        intensities = z

    mesh = {
        "type": "mesh3d",
        "x": x,
        "y": y,
        "z": z,
        "colorscale": colorscale,
        "intensity": intensities,
        "flatshading": flatshading,
        "i": I,
        "j": J,
        "k": K,
        "opacity":opacity,
        "name": "",
        "showscale": showscale,
        "lighting": {
            "ambient": 0.18,
            "diffuse": 1,
            "fresnel": 0.1,
            "specular": 1,
            "roughness": 0.1,
            "facenormalsepsilon": 1e-6,
            "vertexnormalsepsilon": 1e-12,
        },
        "lightposition": {"x": 100, "y": 200, "z": 0},
    }

    if showscale:
        mesh["colorbar"] = {"thickness": 20, "ticklen": 4, "len": 0.75}

    return [mesh]



def create_mesh_data(obj= read_mniobj("human_brain.obj"),atlas_data = None,option=None):
    vertices, faces = obj
    with open("data/fs-atlas.txt", "r") as output:
        for line in output:
            intensities = line.split(',')
            intensities = [int(i) for i in intensities]
    if atlas_data != None:
        intensities = [atlas_data[i] for i in intensities]
    if option == 'trans':
        data = plotly_triangular_mesh(
        vertices, faces, intensities, colorscale = Transparent_colorscale, opacity=0.1)
    else:
        data = plotly_triangular_mesh(
            vertices, faces, intensities#, colorscale=default_colorscale
        )

    data[0]["name"] = "Brain visualization"
    return data

def create_3D_connectivity(atlas= None,data=None):
    if data == None:
        data = []
        with open("data/connectivity.csv",'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append([float(i) for i in row])
    x,y,z = io.loadmat('data/connectivity.mat')['talairach_66'].T
    if atlas == None:
        datas = [go.Scatter3d(x=x,y=y,z=z,
                marker=dict(size=5, color='rgb(50,50,50)'),opacity=0.8)]
    else:
        datas = [go.Scatter3d(x=x,y=y,z=z,
                marker=dict(size=5, color='rgb(50,50,50)'),opacity=0.8),
                go.Scatter3d(x=[x[atlas]],y=[y[atlas]],z=[z[atlas]],
                marker=dict(size=8, color='rgb(200,0,0)'),opacity=1)
                ]

    for i in range(len(data)):
        for j in range(i+1,len(data[i])):
            if data[i][j] != 0:
                if i == atlas or j == atlas:
                    lineColor = 'rgb(200,0,0)'
                else:
                    lineColor = 'rgb(100,100,0)'
                datas.append(go.Scatter3d(x=[x[i],x[j]],y=[y[i],y[j]],z=[z[i],z[j]],
                                        marker=dict(
                                        size=0,
                                    ),
                                    opacity=0.8,                                
                                    line=dict(
                                        color=lineColor,
                                        width=data[i][j]*100
                                    )))
    datas.append(create_mesh_data(option='trans')[0])
    return go.Figure(data=datas, layout =  plot_layout,)

# Make data for circos graph
def get_circos_data(data=None):
    if data == None:
        data = []
        with open("data/connectivity.csv",'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append([float(i) for i in row])
    # Data of Connectivity

    data_size = 40000                    # 100, 3, 10, 1
    excel_file = pd.read_excel('data/Hagmann_66regions.xlsx')


    C_DATA = dict()
    cytobands = []
    chords = []
    grch37=[
        {'id':"1", 'label':'Part 1', 'color':"#ff0000",'len':80000},
        {'id':"2", 'label':'Part 2', 'color':"#ff8c00",'len':90000},
        {'id':"3", 'label':'Part 3', 'color':"#ffff00",'len':130000},
        {'id':"4", 'label':'Part 4', 'color':"#008000",'len':140000},
        {'id':"5", 'label':'Part 5', 'color':"#0000ff",'len':110000},
        {'id':"6", 'label':'Part 6', 'color':"#4b0082",'len':110000},
    ]


    COLOR = []
    for i in range(6):
        r = int('0x'+grch37[i]['color'][1:3],16)
        g = int('0x'+grch37[i]['color'][3:5],16)
        b = int('0x'+grch37[i]['color'][5:7],16)
        c = []
        for j in range(grch37[i]['len']//10000):
            rj = format(r+(256-r)*(6+j)//((grch37[i]['len']//10000)+10),'02x')
            gj = format(g+(256-g)*(6+j)//((grch37[i]['len']//10000)+10),'02x')
            bj = format(b+(256-b)*(6+j)//((grch37[i]['len']//10000)+10),'02x')
            c.append('#'+rj+gj+bj)
        COLOR.append(c)

    base = np.zeros(66)
    f = np.zeros(7)
    for i in range(66):
        p = excel_file['Module number'][i]
        base[i] = f[p]
        f[p] = f[p]+10000

    filled = np.zeros(6)
    c = copy.deepcopy(COLOR)
    for i in range(66):
        p = excel_file['Module number'][i]
        cytobands.append({'name':excel_file['Full Brain regions'][i], 'block_id':str(p),'start':int(filled[p-1]), 'end':int(filled[p-1])+10000,'color':c[p-1][0]})
        filled[p-1] = filled[p-1]+10000
        del c[p-1][0]


    cytobands_out =[]
    for i in range(6):
        cytobands_out.append({'name':grch37[i]['label'], 'block_id':grch37[i]['id'],'start':0, 'end':grch37[i]['len'],'color':grch37[i]['color']})

    for i in range(len(data)):
        for j in range(i+1,len(data[i])):
            if data[i][j] != 0:
                chords.append({'color':'#00000022','id' : i,\
                            'source':{'id':str(excel_file['Module number'][i]),'start' : int(base[i])+5000, 'end' : 5000+int(base[i]+int(data[i][j]*data_size))},\
                            'target':{'id':str(excel_file['Module number'][j]),'start' : int(base[j])+5000, 'end' : 5000+int(base[j]+int(data[i][j]*data_size))}})
    C_DATA['GRCh37']=grch37
    C_DATA['cytobands']=cytobands
    C_DATA['cytobands_out']=cytobands_out
    C_DATA['chords'] = chords
    return C_DATA, COLOR

CIRCOS_DATA,COLOR=get_circos_data()

def get_circos(atlas=None,data=None):
    C_DATA,COLOR = get_circos_data(data)
    if atlas != None:
        for i in range(len(C_DATA['chords'])):
            if C_DATA['chords'][i]['id'] == atlas:
                C_DATA['chords'][i]['color'] = '#000000ff'
            else:
                C_DATA['chords'][i]['color'] = '#00000022'
        c = copy.deepcopy(COLOR)
        for i in range(66):
            p = excel_file['Module number'][i]
            C_DATA['cytobands'][i]['color'] = c[p-1][0]
            if i == atlas:
                C_DATA['cytobands'][i]['color'] = C_DATA['GRCh37'][p-1]['color']
            del c[p-1][0]
        
    return dash_bio.Circos(
    id='main-circos',selectEvent={'0': 'hover', '1': 'click'},
            layout=C_DATA['GRCh37'],
            config={
                'innerRadius': 240,
                'outerRadius': 300,
                'ticks': {'display': False, 'labelDenominator': 10000},
                'labels': {
                    'position': 'center',
                    'display': False,
                    'size': 6,
                    'color': '#000',
                    'radialOffset': 70,
                },
            },
            tracks=[
                {
                    'type': 'HIGHLIGHT',
                    'data': C_DATA['cytobands'],
                    'config': {
                        'innerRadius': 240,
                        'outerRadius': 270,
                        #'opacity': 0.3,
                        'tooltipContent': {'name': 'name'},
                        'color': {'name': 'color'},
                    },
                },
                {
                    'type': 'HIGHLIGHT',
                    'data': C_DATA['cytobands_out'],
                    'config': {
                        'innerRadius': 270,
                        'outerRadius': 300,
                        #'opacity': 0.3,
                        'tooltipContent': {'name': 'name'},
                        'color': {'name': 'color'},
                    },
                },
                {
                    'type': 'CHORDS',
                    'data': C_DATA['chords'],
                    'config': {
                        'logScale': False,
                        #'opacity': {'value' : 'opacity'},
                        'color': {'name': 'color'},
                        'tooltipContent': {
                            'source': 'source',
                            'sourceID': 'id',
                            'target': 'target',
                            'targetID': 'id',
                            'targetEnd': 'end',
                        },
                    },
                },
            ],
            size=750,
        )
