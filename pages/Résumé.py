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
	__name__,path="/"	
)

boto3.setup_default_session(profile_name="spim-dev")
s3client = boto3.client('s3', endpoint_url="http://10.172.104.10:12290")
s3client.download_file('spim-dev-validation', 'data.csv', './data/data.csv')
data = pd.read_csv('./data/data.csv', index_col=False)
data = data[[
    'Categorie', 'Total.Standard', 'VP.Standard', 'FN.Standard', 'Total.Ech',
    'FP.Ech', 'Rappel', 'Precision', 'Fscore', 'Version', 'Date',
    'Environnement', 'Reference', 'Outils'
]]

df = data


def loss(colname):
    loss_gain = {
        "loss": [i * 0 for i in range(len(colname.values))],
        "gain": [i * 0 for i in range(len(colname.values))]
    }
    for i in range(len(colname.values)):
        for j in range(i + 1, len(colname.values)):
            if colname.values[i] > colname.values[j]:
                loss_gain['loss'][j] = Decimal(colname.values[i] -
                                               colname.values[j])
                loss_gain['gain'][j] = Decimal(0)
            if colname.values[i] < colname.values[j]:
                loss_gain['gain'][j] = Decimal(colname.values[j] -
                                               colname.values[i])
                loss_gain['loss'][j] = Decimal(0)
            if colname.values[i] == colname.values[j]:
                loss_gain['loss'][j] = Decimal(0)
                loss_gain['gain'][j] = Decimal(0)
    return loss_gain


layout = html.Div(
    style={'backgroundColor': '#F5F5F5'},
    children=[
         html.Div(style={"text-align": "center"},
                 children=[
                     html.Div([
                         html.Label(['Categorie'],
                                    style={
                                        'font-weight': 'bold',
                                        "text-align": "center"
                                    }),
                         dcc.Dropdown(df['Categorie'].unique(),
                                      'Variant_type',
                                      id='vartype',
                                      style={
                                          'font-weight': 'bold',
                                          "text-align": "center",
                                          'backgroundColor': '#F8F8FF'
                                      })
                     ],
                              style={
                                  'width': '10%',
                                  'display': 'inline-block'
                              }),
                     html.Div([
                         html.Label(['Version de pipeline'],
                                    style={
                                        'font-weight': 'bold',
                                        "text-align": "center",
                                        "margin-left": "30px",
                                    }),
                         dcc.Dropdown(df['Version'].unique(),
                                      'Version pipeline',
                                      id='versionslider',
                                      style={
                                          'font-weight': 'bold',
                                          "text-align": "center",
                                          'backgroundColor': '#F8F8FF',
                                          "margin-left": "15px"
                                      },
                                      multi=True)
                     ],
                              style={
                                  'width': '10%',
                                  'display': 'inline-block'
                              }),
                     html.Div([
                         html.Label([html.A('Référence', href='https://www.nature.com/articles/sdata201625/tables/3')],
                                    style={
                                        'font-weight': 'bold',
                                        "text-align": "center",
                                        "margin-left": "30px"
                                    }),
                         dcc.Dropdown(df['Reference'].unique(),
                                      'reference',
                                      id='ref',
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
                                        "text-align": "center",
                                        "margin-left": "30px"
                                    }),
                         dcc.Dropdown(df['Environnement'].unique(),
                                      'Environnement',
                                      id='env',
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
                                        "text-align": "center",
                                        "margin-left": "30px"
                                    }),
                         dcc.Dropdown(df['Date'].unique(),
                                      'date',
                                      id='date',
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
        dash_table.DataTable(df.to_dict('records'), [{
            "name": i,
            "id": i
        } for i in df.columns],
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
            dcc.Graph(id='variant graphique',
                      style={
                          'width': '39%',
                          'height': '1000px',
                          'display': 'inline-block',
                          "margin-left": "15px"
                      }),
            dcc.Graph(id='comparaison pipeline',
                      style={
                          'width': '57%',
                          'height': '1000px',
                          'display': 'inline-block',
                          "margin-left": "20px"
                      })
        ])
    ])


@callback(Output('variant graphique', 'figure'),
              Output('comparaison pipeline', 'figure'),
              Input('vartype', 'value'), Input('versionslider', 'value'),
              Input('date', 'value'), Input('env', 'value'),
              Input('ref', 'value'))
def update_graph(variant_type, version_value, date, env, ref):
    dff = df[(df['Version'] == version_value[0])
             & (df['Categorie'] == variant_type) & (df['Date'] == date) &
             (df['Environnement'] == env) & (df['Reference'] == ref)]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=dff['Categorie'],
               y=dff['Precision'],
               name='Precision',
               marker=dict(color='#00008B')))
    fig.add_trace(
        go.Bar(x=dff['Categorie'],
               y=dff['Rappel'],
               name='Rappel',
               marker=dict(color='#696969')))
    fig.add_trace(
        go.Bar(x=dff['Categorie'],
               y=dff['Fscore'],
               name='F1 Score',
               marker=dict(color='#BDB76B')))
    fig.update_layout(margin={
        'l': 40,
        'b': 40,
        't': 10,
        'r': 0
    },
                      hovermode='closest')

    fig.update_xaxes(title="Type de Variant")

    fig.update_yaxes(title="Metrique", type='log')
    #

    dff2 = df[(df['Version'].isin(list(version_value))) 
              & (df['Categorie'] == variant_type) & (df['Reference'] == ref) & (df['Environnement'] == env)] 
    p = pd.DataFrame.from_dict(loss(dff2["Precision"]), orient='index')
    p = p.astype('float')
    p = p.transpose()
    r = pd.DataFrame.from_dict(loss(dff2["Rappel"]), orient='index')
    r = r.astype('float')
    r = r.transpose()
    f1 = pd.DataFrame.from_dict(loss(dff2["Fscore"]), orient='index')
    f1 = f1.astype('float')
    f1 = f1.transpose()
    texte1 = []
    texte1_2 = []
    for i, j, k in zip(dff2["Precision"], p["gain"], p["loss"]):
        texte1.append('<b>' + "Valeur:{},Delta:{}".format(i, j) + '</b>')
        texte1_2.append('<b>' + "Valeur:{},Delta:{}".format(i, -1 * k) +
                        '</b>')
    texte2 = []
    texte2_2 = []
    for i, j, k in zip(dff2["Rappel"], r["gain"], r["loss"]):
        texte2.append('<b>' + "Valeur:{},Delta:{}".format(i, j) + '</b>')
        texte2_2.append('<b>' + "Valeur:{},Delta:{}".format(i, -1 * k) +
                        '</b>')
    texte3 = []
    texte3_2 = []
    for i, j, k in zip(dff2["Fscore"], f1["gain"], f1["loss"]):
        texte3.append('<b>' + "Valeur:{},Delta:{}".format(i, j) + '</b>')
        texte3_2.append('<b>' + "Valeur:{},Delta:{}".format(i, -1 * k) +
                        '</b>')
    fig2 = make_subplots(rows=1,
                         cols=3,
                         shared_yaxes=True,
                         subplot_titles=('Précision', 'Rappel', 'Fscore'),
                         horizontal_spacing=0.15)
    fig2.add_trace(go.Bar(x=dff2["Precision"],
                          y=dff2["Version"],
                          name="Valeur",
                          orientation="h",
                          width=0.3,
                          marker=dict(color='#00008B',
                                      line=dict(width=2, color='black')),
                          hovertext=dff2["Precision"],
                          legendgroup="group1",
                          hoverinfo='text',
                          textfont=dict(size=14,
                                        family="Times New Roman",
                                        color='black'),
                          showlegend=True),
                   row=1,
                   col=1)
    #gain prec
    fig2.add_trace(go.Bar(x=-1 * p["gain"],
                          y=dff2["Version"],
                          name='Delta',
                          width=0.3,
                          marker=dict(color='#5F9EA0',
                                      line=dict(width=1, color='black')),
                          orientation="h",
                          text=texte1,
                          textposition='inside',
                          hovertext=p["gain"],
                          legendgroup="group2",
                          hoverinfo='text',
                          textfont=dict(size=14,
                                        family="Times New Roman",
                                        color='black'),
                          showlegend=True,
                          base=dff2["Precision"]),
                   row=1,
                   col=1)
    #loss_prec
    fig2.add_trace(go.Bar(x=p["loss"],
                          y=dff2["Version"],
                          name='Delta',
                          width=0.3,
                          marker=dict(color='white',
                                      opacity=0.4,
                                      line=dict(width=0.5, color='red')),
                          orientation="h",
                          text=texte1_2,
                          textposition='inside',
                          legendgroup="group2",
                          hoverinfo='skip',
                          textfont=dict(size=14,
                                        family="Times New Roman",
                                        color='black'),
                          showlegend=False,
                          base=dff2["Precision"],
                          opacity=0.8),
                   row=1,
                   col=1)
    #Rappel
    fig2.add_trace(go.Bar(x=dff2["Rappel"],
                          y=dff2["Version"],
                          orientation="h",
                          width=0.3,
                          marker=dict(color='#00008B',
                                      line=dict(width=2, color='black')),
                          hovertext=dff2["Rappel"] - r["gain"],
                          hoverinfo='text',
                          textfont=dict(size=14,
                                        family="Times New Roman",
                                        color='black'),
                          showlegend=False),
                   row=1,
                   col=2)
    #gain Rappel
    fig2.add_trace(go.Bar(x=-1 * r["gain"],
                          y=dff2["Version"],
                          width=0.3,
                          marker=dict(color='#5F9EA0',
                                      line=dict(width=1, color='black')),
                          orientation="h",
                          text=texte2,
                          textposition='inside',
                          hovertext=r["gain"],
                          hoverinfo='text',
                          textfont=dict(size=14,
                                        family="Times New Roman",
                                        color='black'),
                          showlegend=False,
                          base=dff2["Rappel"]),
                   row=1,
                   col=2)
    #loss_Rappel
    fig2.add_trace(go.Bar(x=r["loss"],
                          y=dff2["Version"],
                          name='Delta',
                          width=0.3,
                          marker=dict(color='white',
                                      opacity=0.4,
                                      line=dict(width=0.5, color='red')),
                          orientation="h",
                          text=texte2_2,
                          textposition='inside',
                          legendgroup="group2",
                          hoverinfo='skip',
                          textfont=dict(size=14,
                                        family="Times New Roman",
                                        color='black'),
                          showlegend=False,
                          base=dff2["Rappel"],
                          opacity=0.8),
                   row=1,
                   col=2)
    #f1
    fig2.add_trace(go.Bar(x=dff2["Fscore"],
                          y=dff2["Version"],
                          orientation="h",
                          width=0.3,
                          marker=dict(color='#00008B',
                                      line=dict(width=2, color='black')),
                          hovertext=dff2["Fscore"] - f1["gain"],
                          hoverinfo='text',
                          textfont=dict(size=14,
                                        family="Times New Roman",
                                        color='black'),
                          showlegend=False),
                   row=1,
                   col=3)

    #gain f1
    fig2.add_trace(go.Bar(x=-1 * f1["gain"],
                          y=dff2["Version"],
                          width=0.3,
                          marker=dict(color='#5F9EA0',
                                      line=dict(width=1, color='black')),
                          orientation="h",
                          text=texte3,
                          textposition='inside',
                          hovertext=f1["gain"],
                          legendgroup="group2",
                          hoverinfo='text',
                          textfont=dict(size=14,
                                        family="Times New Roman",
                                        color='black'),
                          showlegend=False,
                          base=dff2["Fscore"]),
                   row=1,
                   col=3)
    #loss_f1
    fig2.add_trace(go.Bar(x=f1["loss"],
                          y=dff2["Version"],
                          name='Delta',
                          width=0.3,
                          marker=dict(color='white',
                                      opacity=0.4,
                                      line=dict(width=0.5, color='red')),
                          orientation="h",
                          text=texte3_2,
                          textposition='inside',
                          legendgroup="group2",
                          hoverinfo='skip',
                          textfont=dict(size=14,
                                        family="Times New Roman",
                                        color='black'),
                          showlegend=False,
                          base=dff2["Fscore"],
                          opacity=0.8),
                   row=1,
                   col=3)
    fig2.layout["xaxis1"].update(type="log",
                                 tickangle=45,
                                 ticks="outside",
                                 tickwidth=1,
                                 tickcolor='crimson')
    fig2.layout["xaxis2"].update(type="log",
                                 tickangle=45,
                                 ticks="outside",
                                 tickwidth=1,
                                 tickcolor='crimson')
    fig2.layout["xaxis3"].update(type="log",
                                 tickangle=45,
                                 ticks="outside",
                                 tickwidth=1,
                                 tickcolor='crimson')
    fig2.layout["yaxis1"].update(tickangle=45,
                                 ticks="outside",
                                 tickwidth=1,
                                 tickcolor='crimson')
    #fig2.layout["yaxis2"].update(tickangle=45,ticks="outside",
    #                            tickwidth=1, tickcolor='crimson')
    #fig2.layout["yaxis3"].update(tickangle=45,ticks="outside",
    #                            tickwidth=1, tickcolor='crimson')
    fig2['layout']['xaxis']['title'] = 'Valeur'
    fig2['layout']['yaxis']['title'] = 'Version'
    fig2['layout']['xaxis2']['title'] = 'Valeur'
    #fig2['layout']['yaxis2']['title']='Version'
    fig2['layout']['xaxis3']['title'] = 'Valeur'
    #fig2['layout']['yaxis3']['title']='Version'
    fig2.update_layout(barmode='relative', hovermode="y", title=variant_type)
    return fig, fig2

