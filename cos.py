import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import inspect

import pandas as pd
import plotly.figure_factory as ff
import numpy as np
import math
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import json
import dash  # (version 1.12.0) pip install dash
import geopandas as gpd


LOGO = "https://raw.githubusercontent.com/lperozzi/personale_web/preview/data/logo_white.png"
cos = pd.read_csv('static/cos.csv')

#  define earth radius (in meters) for hexagone resolution calculation)
earth_radius = 6.371e6
zoom=11
opacity=0.5



###################################################
#############  Start of the Dash app #############
###################################################
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.LUX],
                title='GECOS | Geothermal chance of success',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, height=device-height, initial-scale=1.0, maximum-scale=1.2'}]
                )




###################################################
#############  Header /Navigation bar #############
###################################################
navbar = dbc.Navbar(
                [
                html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                                [   dbc.Col(html.Img(src=LOGO, height="30px")),
                                    dbc.Col(dbc.NavbarBrand("| Hexbin Map example", className="ml-2")),
                                ],
                                align="center",
                                no_gutters=True,
                                ),
                        href="https://www.geomaap.io/about",
                    ),
                ],
                color="dark",
                dark=True,
                className="mb-4",
)


###################################################
#############  Controls ##########################
###################################################

targetdepth_tab = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Target depth"),
            dcc.RangeSlider(
                            id='TargetDepth',
                            marks={
                                0: {'label': '0', 'style': {'fontSize': "0.6rem"}},
                                300: {'label': '300 m', 'style': {'fontSize': "0.6rem"}},     # key=position, value=what you see
                                500: {'label': '', 'style': {'fontSize': "0.6rem"}},
                                1000: {'label': '1000 m', 'style': {'fontSize': "0.6rem"}},
                                1500: {'label': '', 'style': {'fontSize': "0.6rem"}},
                                2000: {'label': '2000 m', 'style': {'fontSize': "0.6rem"}},
                                3000: {'label': '', 'style': {'fontSize': "0.6rem"}},
                                4000: {'label': '4000 m', 'style': {'fontSize': "0.6rem"}},
                                },
                            step=20,                # number of steps between values
                            min=0,
                            max=4000,
                            value=[0,4000],     # default value initially chosen4
                            dots=True,             # True, False - insert dots, only when step>1
                            allowCross=False,      # True,False - Manage handle crossover
                            disabled=False,        # True,False - disable handle
                            pushable=2,            # any number, or True with multiple handles
                            updatemode='mouseup',  # 'mouseup', 'drag' - update value method
                            included=True,         # True, False - highlight handle
                            vertical=False,        # True, False - vertical, horizontal slider
                            verticalHeight=900,    # hight of slider (pixels) when vertical=True
                            className='None',
                            tooltip={'always_visible':False,  # show current slider values
                                    'placement':'bottom'},
                            ),
        ]
    )
)

colorscale_names = ['Greys','RdBu','Viridis','Magma','Jet','IceFire']

control_tab = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6("Colormap"),
                    dcc.Dropdown(
                        id='colorscale', 
                        options=[{"value": x, "label": x} 
                                for x in colorscale_names],
                        value='IceFire',
                        style={'margin-bottom':'10px'}
                    ), 
                ]
            ),
         ),
        dbc.Card(   
            dbc.CardBody(
                [
                    html.H6("Hexbin resolution"),
                    dcc.Dropdown(
                        id="resolution",
                        options=[
                            {'label': '300 m', 'value': 300},
                            {'label': '500 m', 'value': 500},
                            {'label': '750 m', 'value': 750},
                            {'label': '1000 m', 'value': 1000},
                            {'label': '2000 m', 'value': 2000},
                        ],
                        value=500,
                        clearable=False
                    ) 
                ]
            )
        ),
    ]
)

credits_tab = dbc.Card(
    dbc.CardBody(
        dcc.Markdown(
            """
            Made with love with Dash

            Realization: [geomaap.io](https://www.geomaap.io/about)
        
            """
        ),
    ),
    className="mt-0",
)

###################################################
#############  Right layout (=Maps) ###############
###################################################

data_density_map_component = dbc.Card(
    [
        dbc.CardHeader(
            html.H3("Data density map")), 
            dbc.CardBody(
                [
                    dcc.Markdown(
                        """
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut nec ultrices risus, eleifend aliquam dolor. Curabitur quis libero quis dui volutpat iaculis. Phasellus pellentesque mi vitae mauris scelerisque, id aliquam lacus mattis. Vestibulum dolor est, consequat sed elit ut, convallis euismod risus. Curabitur id ex diam. Etiam in augue id.

                        """
                    ),
                    dcc.Graph(
                        id='data_density' , 
                        style={'height': 800},
                        ), 
                ],
                style={'padding':'0.5'}
            )
    ], 
    className="my-2", 
    style={'height': 980}
)

data_cos_component = dbc.Card(
    [
        dbc.CardHeader(
            html.H3("Data density map")), 
            dbc.CardBody(
                [
                    dcc.Markdown(
                        """
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut nec ultrices risus, eleifend aliquam dolor. Curabitur quis libero quis dui volutpat iaculis. Phasellus pellentesque mi vitae mauris scelerisque, id aliquam lacus mattis. Vestibulum dolor est, consequat sed elit ut, convallis euismod risus. Curabitur id ex diam. Etiam in augue id.

                        """
                    ),
                    dcc.Graph(
                        id='data_cos' , 
                        style={'height': 800},
                        # responsive=True
                        ), 
                ],
                style={'padding':'0.5'}
            )
    ], 
    className="my-2", 
    style={'height': 980}
)


fig_tab = dbc.Tabs(
    [
        dbc.Tab(data_density_map_component, label="Data density map",active_label_style={"font-weight":"800","color": "#00AEF9"}),
        dbc.Tab(data_cos_component, label="COS map",active_label_style={"font-weight":"800","color": "#00AEF9"}),

    ]
)

###################################
######  Layout of Dash app ########
###################################

app.layout = dbc.Container(
    [
        navbar,
        dbc.Row(
            [
                
                dbc.Col(  # left layout
                    
                    [
                    dbc.CardHeader("Data control"),
                    targetdepth_tab, 
                    control_tab,
                    dbc.CardHeader("Credits"),
                    credits_tab,
                    ], 
                        width=4),

                dbc.Col( # right layout
                    [
                    fig_tab,
                    ],
                    width=8,
                ),
            ]
        ),
    ],
    fluid=True,
)

###################################
######  Data density Map ########
###################################

@app.callback(
    Output('data_density', 'figure'),
    [
     Input('resolution', 'value'),
     Input('TargetDepth', 'value'),
     Input("colorscale", "value"),
    ]
)
def update_data_density(resolution, depth, scale):

    dff= cos.copy()
    dff = dff[(dff["TARGET DEP"] >= depth[0]) & (dff["TARGET DEP"] <= depth[1])]
    heg_size = -1* ((dff.X.max() - dff.X.min()) / resolution * np.pi / 180 * earth_radius  * np.cos(dff.Y.mean()))
    heg_size = math.floor(heg_size)  # define hegsize dimension
    

    fig_data_density = ff.create_hexbin_mapbox(data_frame=dff, 
                                        lat="Y", lon="X",
                                        nx_hexagon=heg_size, 
                                        opacity=opacity, 
                                        labels={"color": "Density index"},
                                        color="SCORE", 
                                        agg_func=np.sum, 
                                        mapbox_style='carto-positron',
                                        color_continuous_scale=scale,
                                        show_original_data=False, 
                                        original_data_marker=dict(opacity=0.6, size=4, color="black"),
                                        min_count=1,
                                        zoom=10.5,
                                        center= {"lon": 6.13, "lat": 46.22}
                                        )
    
    fig_data_density.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                    
                            showlegend=False,
                            coloraxis_showscale=False,  
                            hoverlabel=dict(
                                bgcolor="#3a3a3b",
                                font_color='white',
                                # color='white',
                                font_size=16,
                                font_family="Nunito Sans"
                            )
                         )
    fig_data_density.data[0].hovertemplate = "<span style='font-size:1.2rem; font-weight=400'>Data density index = %{z:,.0f}</span><br><br>"

    return fig_data_density

###################################
######  Cos Map ########
###################################


@app.callback(
    Output('data_cos', 'figure'),
    [
     Input('resolution', 'value'),
     Input('TargetDepth', 'value'),
     Input("colorscale", "value"),
    ]
)
def update_data_cos(resolution, depth, scale):

    dff= cos.copy()
    dff = dff[(dff["TARGET DEP"] >= depth[0]) & (dff["TARGET DEP"] <= depth[1])]
    heg_size = -1* ((dff.X.max() - dff.X.min()) / resolution * np.pi / 180 * earth_radius  * np.cos(dff.Y.mean()))
    heg_size = math.floor(heg_size)  # define hegsize dimension
    

    fig_cos = ff.create_hexbin_mapbox(data_frame=dff, 
                                        lat="Y", lon="X",
                                        nx_hexagon=heg_size, 
                                        opacity=opacity, 
                                        labels={"color": "Density index"},
                                        color="COS", 
                                        agg_func=np.sum, 
                                        mapbox_style='carto-positron',
                                        color_continuous_scale=scale,
                                        show_original_data=False, 
                                        original_data_marker=dict(opacity=0.6, size=4, color="black"),
                                        min_count=1,
                                        zoom=10.5,
                                        center= {"lon": 6.13, "lat": 46.22}
                                        )
    
    fig_cos.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                    
                            showlegend=False,
                            coloraxis_showscale=False,  
                            hoverlabel=dict(
                                bgcolor="#3a3a3b",
                                font_color='white',
                                # color='white',
                                font_size=16,
                                font_family="Nunito Sans"
                            )
                         )
    fig_cos.data[0].hovertemplate = "<span style='font-size:1.2rem; font-weight=400'>COS index = %{z:,.0f}</span><br><br>"

    return fig_cos

if __name__ == "__main__":
    app.run_server(debug=True)
