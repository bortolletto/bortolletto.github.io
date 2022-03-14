#!/usr/bin/env python
# coding: utf-8

# In[1]:



#-------------------------------------------------------
mapbox_access_token = "pk.eyJ1IjoiYm9ydG9sbGV0dG8iLCJhIjoiY2wwcXd5ZDI0MjNuZTNrbzN6dXN1dmk5cSJ9.DxwSG1KGXbjEaHSwO-qydQ"
import pandas as pd
import numpy as np
import dash                     #(version 1.0.0)
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datashader as ds
import plotly.offline as py     #(version 4.4.1)
import plotly.graph_objs as go
import datashader.transfer_functions as tf
from colorcet import fire

df = pd.read_csv("/home/felipe.bortolletto/anomalias_latlong.csv")
df.columns = ["Lon","Lat","Anomalia","Nome"]


# In[ ]:




app = dash.Dash(__name__)

blackbold={'color':'black', 'font-weight': 'bold'}

app.layout = html.Div([
#---------------------------------------------------------------
# Map_legen + Borough_checklist + Recycling_type_checklist + Web_link + Map
    html.Div([
        html.Div([

            # Borough_checklist
            html.Label(children=['Bacia: '], style=blackbold),
            dcc.Checklist(id='Bacia',
                    options=[{'label':str(b),'value':b} for b in sorted(df['Nome'].unique())],
                    value=[b for b in sorted(df['Nome'].unique())],
            ),
            
            html.Br(),
            html.Label(['Website:'],style=blackbold),
            html.Pre(id='web_link', children=[],
            style={'white-space': 'pre-wrap','word-break': 'break-all',
                 'border': '1px solid black','text-align': 'center',
                 'padding': '12px 12px 12px 12px', 'color':'blue',
                 'margin-top': '3px'}
            ),

        ], className='three columns'
        ),

        # Map
        html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
                style={'background':'#00FC87','padding-bottom':'2px','padding-left':'2px','height':'100vh'}
            )
        ], className='nine columns'
        ),

    ], className='row'
    ),

], className='ten columns offset-by-one'
)

#---------------------------------------------------------------
# Output of Graph
@app.callback(Output('graph', 'figure'),
              [Input('Bacia', 'value')],)
#                Input('Ano', 'value')]
             

def update_figure(Bacia):
    mapbox_access_token = "pk.eyJ1IjoiYm9ydG9sbGV0dG8iLCJhIjoiY2wwcXd5ZDI0MjNuZTNrbzN6dXN1dmk5cSJ9.DxwSG1KGXbjEaHSwO-qydQ"

    
    
    dff = df[(df['Nome'].isin(Bacia))] 
#                 &  (df['type'].isin(chosen_recycling))]



    cvs = ds.Canvas(plot_width=4000, plot_height=4000)

    # # project the longitude and latitude onto the canvas and
    # # map the data to pixels as points
    aggs = cvs.points(dff, x='Lon', y='Lat')

    # # aggs is an xarray object, see http://xarray.pydata.org/en/stable/ for more details
    coords_lat, coords_lon = aggs.coords['Lat'].values, aggs.coords['Lon'].values

    # # Set the corners of the image that need to be passed to the mapbox
    coordinates = [[coords_lon[0], coords_lat[0]],
                   [coords_lon[-1], coords_lat[0]],
                   [coords_lon[-1], coords_lat[-1]],
                   [coords_lon[0], coords_lat[-1]]]


    # # Set the image color, and the legend (how) types
    # # linear (how=linear), logarithmic (how=log), percentile (how=eq_hist)
    img = tf.shade(aggs,cmap=fire)[::-1].to_pil()

    # # Create a quick mapbox figure with plotly
    fig = px.scatter_mapbox(dff, lat='Lat', lon='Lon',color="Anomalia", zoom=6)

    # # Add the datashader image as a mapbox layer image
    fig.update_layout(mapbox_style="carto-darkmatter",
                      mapbox_layers=[
                          {
                        "sourcetype": "image",
                        "source": img,
                        "coordinates": coordinates
                          }
                      ]
    )


    return (fig)

# #--------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





# In[ ]:





# In[ ]:




