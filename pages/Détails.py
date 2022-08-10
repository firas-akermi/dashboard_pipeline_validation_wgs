#!/usr/bin/env python3
#Firas Akermi
#Dashboar juillet 2022
#akermi1996@gmail.com
import pandas as pd
from decimal import Decimal
import boto3
from dash import Dash, dcc, html, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash

dash.register_page(
	__name__,path="/d"	
)
boto3.setup_default_session(profile_name="spim-dev")
s3client = boto3.client('s3', endpoint_url="http://10.172.104.10:12290")
s3client.download_file('spim-dev-validation', 'statistics.csv', './data/statistics.csv')
data = pd.read_csv('./data/statistics.csv', index_col=False)
layout = html.Div(
    style={'backgroundColor': '#F5F5F5'},
    children=[
         html.Div(style={"text-align": "center"},
                 children=[
                     
                     html.Div([
                         html.Label(['Version de pipeline'],
                                    style={
                                        'font-weight': 'bold',
                                        "text-align": "center"
                                    }),
                         dcc.Dropdown(data['Version'].unique(),
                                      'Version pipeline',
                                      id='version',
                                      style={
                                          'font-weight': 'bold',
                                          "text-align": "center",
                                          'backgroundColor': '#F8F8FF',
                                          "margin-left": "15px"
                                      },
                                      multi=False)
                     ],
                              style={
                                  'width': '10%',
                                  'display': 'inline-block'
                              }),
                     html.Div([
                         html.Label(['Référence'],
                                    style={
                                        'font-weight': 'bold',
                                    }),
                         dcc.Dropdown(data['Reference'].unique(),
                                      'reference',
                                      id='reference',
                                      style={
                                          'font-weight': 'bold',
                                          "text-align": "center",
                                          'backgroundColor': '#F8F8FF',
                                          "margin-left": "15px"
                                      },
                                      multi=False)
                     ],
                              style={
                                  'width': '10%',
                                  'display': 'inline-block'
                              }),
                     html.Div([
                         html.Label(['Environnement'],
                                    style={
                                        'font-weight': 'bold',
                                        "text-align": "center"
                                    }),
                         dcc.Dropdown(data['Environnement'].unique(),
                                      'Environnement',
                                      id='envir',
                                      style={
                                          'font-weight': 'bold',
                                          "text-align": "center",
                                          'backgroundColor': '#F8F8FF',
                                          "margin-left": "15px"
                                      },
                                      multi=False)
                     ],
                              style={
                                  'width': '10%',
                                  'display': 'inline-block'
                              }),
                     html.Div([
                         html.Label(['Date de validation'],
                                    style={
                                        'font-weight': 'bold',
                                        "text-align": "center"
                                    }),
                         dcc.Dropdown(data['Date'].unique(),
                                      'date',
                                      id='d',
                                      style={
                                          'font-weight': 'bold',
                                          "text-align": "center",
                                          'backgroundColor': '#F8F8FF',
                                          "margin-left": "15px"
                                      },
                                      multi=False)
                     ],
                              style={
                                  'width': '10%',
                                  'display': 'inline-block'
                              })
                 ]),
         dash_table.DataTable(data.to_dict('records'), [{
            "name": i,
            "id": i
        } for i in data.columns],
                             style_table={
                                 'width': '100%',
                                 'height': '200px',
                                 'overflowY': 'scroll',
                                 'padding': '40px 20px 20px 20px'
                             },
                             style_header={
                                 'fontWeight': 'bold',
                                 'border': 'thin lightgrey solid',
                                 'backgroundColor': '#8f8f8f',
                                 'color': '#ffffff'
                             },
                             style_cell={
                                 'fontFamily': 'Open Sans',
                                 'textAlign': 'center',
                                 'width': '150px',
                                 'minWidth': '180px',
                                 'maxWidth': '180px',
                                 'whiteSpace': 'no-wrap',
                                 'overflow': 'hidden',
                                 'textOverflow': 'ellipsis',
                                 'backgroundColor': 'white'
                             },
                             style_data_conditional=[{
                                 'if': {
                                     'row_index': 'odd'
                                 },
                                 'backgroundColor':
                                 '#F8F8FF'
                             }, {
                                 'if': {
                                     'row_index': 'even'
                                 },
                                 'backgroundColor': 'white',
                                 'color': 'black',
                                 'fontWeight': 'bold',
                                 'textAlign': 'center'
                             }],
                             fixed_rows={
                                 'headers': True,
                                 'data': 0
                             }),
        html.Div([
            dcc.Graph(id='graph',
                      style={
                          'width': '98%',
                          'height': '90vh',
                          'display': 'inline-block',
                          "margin-left": "15px",
                          "margin-right": "15px"
                      })
            
        ])
    ])
@callback(Output('graph', 'figure'),
              Input('version','value'),
              Input('d', 'value'),
              Input('envir', 'value'),
              Input('reference', 'value')
              )
def update_graph(version, date, env, ref):
    dff = data[(data['Version'] == version)
              & (data['Date'] == date) &
             (data['Environnement'] == env) & (data['Reference'] == ref)]
    fig = make_subplots(rows=3, cols=3)
    fig.add_trace(go.Bar(x=dff['Categorie'], y=dff['TP'], name='TP'),
                  row=1,
                  col=1)
    fig.add_trace(go.Bar(x=dff['Categorie'], y=dff['FN'], name='FN'),
                  row=1,
                  col=2)
    fig.add_trace(go.Bar(x=dff['Categorie'], y=dff['FP'], name='FP'),
                  row=1,
                  col=3)
    fig.add_trace(go.Bar(x=dff['Categorie'], y=dff['FNp'], name='FNp'),
                  row=2,
                  col=1)
    fig.add_trace(go.Bar(x=dff['Categorie'], y=dff['FNt'], name='FNt'),
                  row=2,
                  col=2)
    fig.add_trace(go.Bar(x=dff['Categorie'], y=dff['FPp'], name='FPp'),
                  row=2,
                  col=3)
    fig.add_trace(go.Bar(x=dff['Categorie'], y=dff['FPt'], name='FPt'),
                  row=3,
                  col=1)
    
    
    fig.update_layout(yaxis=dict(autorange=True))

    fig.update_yaxes(title="Nombre")
    fig.update_layout(margin={
        'l': 40,
        'b': 40,
        't': 10,
        'r': 40
    },hovermode='closest')
    return fig