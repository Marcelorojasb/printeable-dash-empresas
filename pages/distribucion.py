import dash
import plotly.graph_objs as go
import plotly.express as px
from datetime import date # Objetos 'date'
from dash import dcc, html, Input, Output, callback
from plotly.subplots import make_subplots # Múltiples plots en gráficos
from PIL import Image

import pandas as pd
import pathlib
# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
#2.0
dash.register_page(__name__,path='/distribucion')

emp_dict = pd.read_parquet(DATA_PATH.joinpath("cen_emp_dict.parquet"), engine='pyarrow')
dem_df = pd.read_parquet(DATA_PATH.joinpath("demanda.parquet"), engine='pyarrow')
comb_df = pd.read_parquet(DATA_PATH.joinpath("combustible.parquet"), engine='pyarrow')

layout = html.Div(
        [
            # page 1
            html.Div(
                [
                    html.Div([
                        'Seleccione empresa',
                        dcc.Dropdown(id='empresa', options=emp_dict.loc['Empresa'].unique(), value=[emp_dict.loc['Empresa'].unique()[0]], clearable=False, multi=True), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Supuestos"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Los gráficos de esta sección corresponden a costos de combustible con mayor detalle \
                                    y la demanda por mes.",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Combustibles plena carga", className="subtitle padded"),
                                    dcc.Graph(id="comb",)
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 6
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Demanda", className="subtitle padded"),
                                    dcc.Graph(id="dem",)
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                ],
                className="letterpage",
            ),
        ],
        className="page",
    )

@callback(
    [Output(component_id='dem',component_property='figure'),
     Output(component_id='comb', component_property='figure'),
    ],
    Input(component_id='empresa',component_property='value'))
def update_dropdown(empresa):
    options = emp_dict.loc[:,emp_dict.loc['Empresa',:].isin(empresa)].columns
    cen_df = comb_df.loc[(comb_df['Nombre'].str.strip()).isin(options)] 
    dem1_df = dem_df.loc[dem_df['Año']==2023] 
    dateA = dem1_df['Año'].unique()[0]
    X = cen_df['Tipo'].values
    text = cen_df['Unidad medida'].values
    fig1 = px.bar(
        x=cen_df['Nombre'],
        y=cen_df['Plena Carga'].astype(float),color=[i for i in X],text=[i for i in text]
    )
    fig1.update_layout(xaxis={'visible': True, 'showticklabels': False})
    fig1.update_layout(yaxis={'visible': True, 'showticklabels': True})
    fig1.update_layout(xaxis_title=None)
    fig1.update_layout(yaxis_title=None)
    # No mostrar leyenda:
    fig1.update_layout(showlegend=False)
    # Edición del hover:
    fig1.update_traces(
        hovertemplate="<br>".join([
            "%{x}" + ': '+ "%{y} %{text}",
        ])
    )
    # Texto en las barras (90°):
    fig1.update_traces(textangle=90)
    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1),
        margin={
                    "r": 30,
                    "t": 30,
                    "b": 30,
                    "l": 30,
                },
        height=350,
        )
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
            go.Bar(x=dem1_df['Mes'], y=dem1_df['Suma de Energía [MWh]'], name="Demanda [MWh]"),
            secondary_y=False,
        )
    fig2.update_xaxes(title_text="Fecha")
    # Título del eje y:
    fig2.update_yaxes(title_text="[MWh]")
    # Hover:
    fig2.update_traces(
    hovertemplate="<br>".join([
        "Fecha: %{x}"+ f"{dateA}",
        "%{y} "+ "USD|MW",
    ]),
    )
    fig2.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1),
    margin={
                "r": 30,
                "t": 30,
                "b": 30,
                "l": 30,
            },
    height=350,
    )
    return fig2, fig1