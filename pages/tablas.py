import dash
from dash import dcc, html, Input, Output, callback, ctx
from utils import make_dash_table
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
#2.0
dash.register_page(__name__,path='/tablas')

df_ret= pd.read_parquet(DATA_PATH.joinpath("engie_retiros.parquet"), engine='pyarrow')
df_mp = pd.read_parquet(DATA_PATH.joinpath("centrales.parquet"), engine='pyarrow')

layout = html.Div(
        [
            # page 5
            html.Div(
                [
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.H6(
                                        ["Datos crudos margen planta"],
                                        className="subtitle padded",
                                    ),
                                    html.Button('Regenerar datos', id='btn1', n_clicks=0),
                                    html.Div(
                                        [
                                            html.Table(
                                                id='table1',
                                                className="tiny-header",
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.H6(
                                        ["Datos crudos retiros Engie"],
                                        className="subtitle padded",
                                    ),
                                    html.Button('Regenerar datos', id='btn2', n_clicks=0),
                                    html.Div(
                                        [
                                            html.Table(
                                                id = 'table2',
                                                className="tiny-header",
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )

@callback(
    Output(component_id='table1',component_property='children'),
    Input(component_id='btn1',component_property='n_clicks'))
def update_dropdown(btn1):
    df_mp1 = df_mp.sample(n=10)
    table1 = make_dash_table(df_mp1)
    return table1

@callback(
    Output(component_id='table2',component_property='children'),
    Input(component_id='btn2',component_property='n_clicks'))
def update_dropdown(btn2):
    df_ret2 = df_ret.sample(n=10)
    table2 = make_dash_table(df_ret2)
    return table2