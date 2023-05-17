# -*- coding: utf-8 -*-
import dash
from dash import dcc, html
from PIL import Image
import pandas as pd
import pathlib
from utils import Header

# get relative data folder
PATH = pathlib.Path(__file__)
DATA_PATH = PATH.joinpath("../data").resolve()


cen_df = pd.read_parquet(DATA_PATH.joinpath("centrales.parquet"), engine='pyarrow')
bar_df = pd.read_parquet(DATA_PATH.joinpath("barras.parquet"), engine='pyarrow')

app = dash.Dash(__name__, use_pages=True, #2.0
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    prevent_initial_callbacks=True, 
    suppress_callback_exceptions=True,

)
app.title = "neocity-empresas"
server = app.server
# "complete" layout



# Describe the layout/ UI of the app
app.layout = html.Div([
        Header(app),
        html.Hr(className='no-print'),
        dash.page_container
])


if __name__ == "__main__":
    app.run_server(debug=True)