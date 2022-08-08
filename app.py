#!/usr/bin/env python
# Firas Akermi
#akermi1996@gmail.com
import pandas as pd
from decimal import Decimal
import boto3
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_labs as dl
import dash 

external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__,
           external_stylesheets=external_stylesheets,
           suppress_callback_exceptions=True,use_pages=True)
navbar = dbc.NavbarSimple(
    
    dbc.DropdownMenu(
        
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Analyses",
    ),
    brand="Validation de pipelines d'appel de variants",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = html.Div(
    [navbar, dash.page_container]
    
)

if __name__ == "__main__":

    app.run(host='127.0.0.1',debug=True,dev_tools_ui=False,dev_tools_props_check=False)
