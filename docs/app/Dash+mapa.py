{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "7c45bce2",
   "metadata": {},
   "outputs": [],
   "source": [
    "#-------------------------------------------------------\n",
    "import pandas as pd\n",
    "import dash                     #(version 1.0.0)\n",
    "from dash import dash_table\n",
    "from dash import dcc\n",
    "from dash import html\n",
    "from dash.dependencies import Input, Output\n",
    "import plotly.express as px\n",
    "import json\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3b3d4609",
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      " * Serving Flask app '__main__' (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)\n",
      "127.0.0.1 - - [18/Mar/2022 15:11:19] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [18/Mar/2022 15:11:19] \"GET /_dash-layout HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [18/Mar/2022 15:11:19] \"GET /_dash-dependencies HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [18/Mar/2022 15:11:19] \"GET /_dash-component-suites/dash/dcc/async-dropdown.js HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [18/Mar/2022 15:11:19] \"GET /_dash-component-suites/dash/dcc/async-graph.js HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [18/Mar/2022 15:11:19] \"GET /_dash-component-suites/dash/dcc/async-plotlyjs.js HTTP/1.1\" 200 -\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "janeiro\n",
      "<class 'str'>\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "127.0.0.1 - - [18/Mar/2022 15:11:33] \"POST /_dash-update-component HTTP/1.1\" 200 -\n"
     ]
    }
   ],
   "source": [
    "app = dash.Dash(__name__)\n",
    "server = app.server\n",
    "df = pd.read_csv(\"medias_municipios.csv\",\n",
    "                   dtype={\"nome\": str})\n",
    "df.columns = [\"fid\",\"gid\",\"codibge\",\"Município\",\"Anomalia\"]\n",
    "df[\"Porcentagem\"] = round(df[\"Anomalia\"]).astype(str)\n",
    "df[\"Porcentagem\"] = df[\"Porcentagem\"]+\"%\"\n",
    "\n",
    "df=df.assign(Mes=\"janeiro\")\n",
    "\n",
    "dx = pd.read_csv(\"Municipios_2020228.csv\")\n",
    "dx.columns = [\"fid\",\"gid\",\"codibge\",\"Município\",\"Anomalia\"]\n",
    "dx[\"Porcentagem\"] = round(dx[\"Anomalia\"]).astype(str)\n",
    "dx[\"Porcentagem\"] = dx[\"Porcentagem\"]+\"%\"\n",
    "\n",
    "dx = dx.assign(Mes=\"fev\")\n",
    "\n",
    "dy = pd.read_csv(\"Municipios_202203.csv\")\n",
    "dy.columns = [\"fid\",\"gid\",\"codibge\",\"Município\",\"Anomalia\"]\n",
    "dy[\"Porcentagem\"] = round(dy[\"Anomalia\"]).astype(str)\n",
    "dy[\"Porcentagem\"] = dy[\"Porcentagem\"]+\"%\"\n",
    "\n",
    "dy = dx.assign(Mes=\"marco\")\n",
    "\n",
    "df = pd.merge(df, dx, how = 'outer')\n",
    "df = pd.merge(df, dy, how = 'outer')\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "pd_dict = pd.DataFrame()\n",
    "pd_dict[\"Anomalia\"] = df[\"Anomalia\"]\n",
    "pd_dict[\"porcentagem\"] = df[\"Porcentagem\"]\n",
    "pd_dict.index = df[\"Anomalia\"]\n",
    "pd_dict.drop(columns=['Anomalia'],inplace = True)\n",
    "dic = pd_dict.to_dict()\n",
    "\n",
    "\n",
    "geojson = json.load(open(\"municipios_media.geojson\"))\n",
    "for i in range(len(geojson['features'])):\n",
    "    geojson['features'][i]['properties']['Município'] = geojson['features'][i]['properties']['nome']\n",
    "coluna={\n",
    "\"fid\":False,\"gid\":False,\"codibge\":False,\"Município\":True,\"Anomalia\":False,\"Porcentagem\" : True ,\"Mes\": False       \n",
    "}\n",
    "\n",
    "#---------------------------------------------------------------\n",
    "# Map_legen + Borough_checklist + Recycling_type_checklist + Web_link + Map\n",
    "\n",
    "app.layout = html.Div([\n",
    "\n",
    "    html.H1(\"Anomalias Paraná\", style={'text-align': 'center'}),\n",
    "\n",
    "    dcc.Dropdown(id=\"slct_year\",\n",
    "                 options=[\n",
    "                     {\"label\": \"Janeiro\", \"value\": \"janeiro\"},\n",
    "                     {\"label\": \"Fevereiro\", \"value\": \"fev\"},\n",
    "                     {\"label\": \"Março\", \"value\": \"marco\"}],\n",
    "                 multi=False,\n",
    "                 value=\"janeiro\",\n",
    "                 style={'width': \"40%\"}\n",
    "                 ),\n",
    "\n",
    "\n",
    "    html.Div(id='output_container', children=[]),\n",
    "    html.Br(),\n",
    "\n",
    "    dcc.Graph(id='my_bee_map', figure={})\n",
    "\n",
    "])\n",
    "\n",
    "\n",
    "#---------------------------------------------------------------\n",
    "# Output of Graph\n",
    "@app.callback(\n",
    "    [Output(component_id='output_container', component_property='children'),\n",
    "     Output(component_id='my_bee_map', component_property='figure')],\n",
    "    [Input(component_id='slct_year', component_property='value')]\n",
    ")\n",
    "def update_graph(option_slctd):\n",
    "    print(option_slctd)\n",
    "    print(type(option_slctd))\n",
    "\n",
    "    container = \"Anomalia do mês de {}\".format(option_slctd)\n",
    "\n",
    "    dff = df.copy()\n",
    "    dff = dff[dff[\"Mes\"] == option_slctd]\n",
    " \n",
    "    fig = px.choropleth_mapbox(dff, geojson=geojson, color=\"Anomalia\",\n",
    "                               locations=\"Município\", featureidkey=\"properties.Município\",\n",
    "                               center={\"lat\": -24, \"lon\": -51},\n",
    "                               color_continuous_scale=px.colors.diverging.BrBG,\n",
    "                               color_continuous_midpoint=0,\n",
    "                               hover_data = coluna,\n",
    "                               opacity = 0.8,\n",
    "                               mapbox_style=\"carto-positron\", zoom=6)\n",
    "    fig.update_layout(margin={\"r\":0,\"t\":0,\"l\":0,\"b\":0})\n",
    "    \n",
    "\n",
    "    return container, fig\n",
    "    #--------------------------------------------------------------\n",
    "if __name__ == '__main__':\n",
    "    app.run_server(debug=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f00abf42",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Site",
   "language": "python",
   "name": "site"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
