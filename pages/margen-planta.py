import dash
import plotly.graph_objs as go
from datetime import date # Objetos 'date'
from dash import dcc, html, Input, Output, callback
from plotly.subplots import make_subplots # Múltiples plots en gráficos
from PIL import Image
from utils import make_dash_table, make_Mplanta_table, make_dataCen_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
#2.0
dash.register_page(__name__,path='/margen-planta')

# Overview data
#df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
#df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))
cen_df = pd.read_parquet(DATA_PATH.joinpath("centrales.parquet"), engine='pyarrow')
bar_df = pd.read_parquet(DATA_PATH.joinpath("barras.parquet"), engine='pyarrow')
cenF_df = pd.read_parquet(DATA_PATH.joinpath("centralesFCTA.parquet"), engine='pyarrow')
barF_df = pd.read_parquet(DATA_PATH.joinpath("barrasFCTA.parquet"), engine='pyarrow')
emp_dict = pd.read_parquet(DATA_PATH.joinpath("cen_emp_dict.parquet"), engine='pyarrow')
plpdate="2023.03"
start_date = date(
    year=int(plpdate[0:4]),
    month=int(plpdate[5:7]),
    day=1
)
end_date = date(
    year=int(plpdate[0:4])+1,
    month=int(plpdate[5:7]),
    day=1
)

#2.0
layout = html.Div(
        [
            # page 1
            html.Div(
                [
                    html.Div([
                        'Seleccione empresa',
                        dcc.Dropdown(id='Emp2', options=emp_dict.loc['Empresa'].unique(), value=emp_dict.loc['Empresa'].unique()[0], clearable=False), # Selección de la simulación
                    ]),
                    html.Div([
                        'Seleccione caso',
                        dcc.Dropdown(id='Caso2', options=['Caso base', 'Caso falla CTA engie'], value='Caso base', clearable=False), # Selección de la simulación
                    ]),
                    html.Div([
                        'Seleccione central',
                        dcc.Dropdown(id = 'Cen2', value=cen_df['cen_nom'].unique()[0]), # Selección de la central (por nombre)
                    ]),
                    html.Div([
                        'Seleccione simulación',
                        dcc.Dropdown(id='Sim2', options=cen_df['Hidro'].unique(), value=cen_df['Hidro'].unique()[0], clearable=False), # Selección de la simulación
                    ]),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Margen Planta"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Ingresos vs costos por central. Debe seleccionar empresas, caso a observar (base o falla), \
                                    central a observar y una simulación.",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    #html.Div([
                        #'Seleccione central',
                        #dcc.Dropdown(id = 'Cen' ,options=cen_df['cen_nom'].unique(), value=cen_df['cen_nom'].unique()[0], clearable=False), # Selección de la central (por nombre)
                    #]),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Datos Planta"], className="subtitle padded"
                                    ),
                                    html.Table(id='datos-planta-table2'),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Ingresos/Costos",
                                        className="subtitle padded",
                                    ),
                                    html.Table(id='m-planta-table2'),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "20px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Ingresos planta", className="subtitle padded"),
                                    dcc.Graph(id="margen_planta2",)
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
                                    html.H6("Costo variable", className="subtitle padded"),
                                    dcc.Graph(id="c_var2",)
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
    [Output(component_id='Cen2',component_property='options')
    ],
    [Input(component_id='Emp2',component_property='value')
    ])
def update_dropdown(empresa):
    options = emp_dict.loc[:,emp_dict.loc['Empresa',:] == empresa].columns
    options = options.values
    options = [options.tolist()]
    return options

@callback(
    [Output(component_id='margen_planta2', component_property='figure'),
     Output(component_id='c_var2', component_property='figure'),
     Output(component_id='m-planta-table2', component_property='children'),
     Output(component_id='datos-planta-table2', component_property='children')],
    [Input(component_id='Caso2',component_property='value'),
     Input(component_id='Cen2', component_property='value'), # Central seleccionada
     Input(component_id='Sim2',component_property='value')])
def update_planta(caso,Cen, Sim):
    # Margen planta 
    df1 = cen_df.loc[cen_df['cen_nom'].str.strip() == Cen.strip()] # Se filtra por nombre de la central
    df1 = df1.loc[df1['Hidro'].str.strip() == Sim.strip()]
    bar = df1['bar_nom'].unique()[0].strip()
    df2 = bar_df.loc[bar_df['bar_nom'].str.strip() == bar]
    df2 = df2.loc[df2['Hidro'].str.strip() == Sim.strip()]
    df1 = df1.sort_values(by=['date']) # Se ordenan los datos por fecha para los gráficos de linea
    df2 = df2.sort_values(by=['date']) # Se ordenan los datos por fecha para los gráficos de linea
    plpdate="2023.03"
    start_date = date(
        year=int(plpdate[0:4]),
        month=int(plpdate[5:7]),
        day=1
    )
    end_date = date(
        year=int(plpdate[0:4])+1,
        month=int(plpdate[5:7]),
        day=1
    )
    # Se crea el primer gráfico (Generación/CMG/ingreso unitario): 
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    # Gráfico de barra de potencia generada
    fig1.add_trace(
        go.Bar(x=df1['date'], y=df1['CenPgen'], name="P generada " +  " [MW]", marker_color='rgb(1,114, 192)'),
        secondary_y=False,
    )
    # Costo marginal de la barra (se muestra el de la primera fecha en la lista):
    fig1.add_trace(
        go.Scatter(x=df2['date'], y=df2['CMgBar'], name="Cmg barra [USD|MWh]", marker_color='#4caf50'),
        secondary_y=True,
    )
    # Ingreso unitario:
    fig1.add_trace(
        go.Scatter(x=df1['date'], y=df1['iu'], name="Ingreso unitario [USD|MWh]"),
        secondary_y=True,
    )
    # Titulo del gráfico:
    #fig.update_layout(
    #title_text="Proyección potencia generada")
    # Título del eje x:
    fig1.update_xaxes(title_text="Fecha")
    # Título del eje y principal:
    fig1.update_yaxes(title_text="[MW]", secondary_y=False)
    # Título del eje y secundario:
    fig1.update_yaxes(title_text="[USD|MWh]", secondary_y=True)
    # Hover eje principal:
    fig1.update_traces(
    hovertemplate="<br>".join([
        "Fecha: %{x}",
        "%{y} "+ "MW",
    ]), secondary_y=False
    )
    # Hover del eje secundario:
    fig1.update_traces(
    hovertemplate="<br>".join([
        "Fecha: %{x}",
        "%{y} "+ "USD|MWh",
    ]), secondary_y=True
    )
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
    # Se agrega el logo:
    #fig.add_layout_image(
    #dict(
        #source=pyLogo,
        #xref="paper", yref="paper",
        #x=1.23, y=1.05,
        #sizex=0.2, sizey=0.2,
        #xanchor="right", yanchor="bottom"
    #)
    #)
    # Se setea el zoom inicial:
    fig1.update_xaxes(type="date", range=[start_date, end_date])

    # Se crea el segundo gráfico (Costo variable):
    fig2 = make_subplots()
    # Se añade gráfico de barras del costo variable de la central:
    fig2.add_trace(
            go.Bar(x=df1['date'], y=df1['CenCVar'], name="Costo variable" + " [USD|MW]", marker_color='rgb(1,114, 192)')
        )
    # Variable pos determina la posición del logo, depende de la cantidad de fechas que se muestre, pues al tener más de una fecha, la leyenda cambia la posición del gráfico
    #if len(plpdate)<=1:
        #pos=1.05
    #else:
        #pos=1.31 # Posición del logo si hay más de una fecha de plp
        #for i in plpdate[1:]: # Se recorren lo plp si hay más de 1
            #cen_aux = df2.loc[df2['plp_date'] == i]
            #fig2.add_trace(
                #go.Bar(x=cen_aux['date'], y=cen_aux['CenCvar'], name="Costo variable " + i[5:7]+ '/' + i[0:4] + " [USD|MW]")
            #)
    # Título del gráfico:
    #fig2.update_layout(
    #title_text="Proyección costo variable")
    # Título del eje x:
    fig2.update_xaxes(title_text="Fecha")
    # Título del eje y:
    fig2.update_yaxes(title_text="[USD|MW]")
    # Hover:
    fig2.update_traces(
    hovertemplate="<br>".join([
        "Fecha: %{x}",
        "%{y} "+ "USD|MW",
    ]),
    )
    # Se agrega el logo:
    #fig2.add_layout_image(
    #dict(
        #source=pyLogo,
        #xref="paper", yref="paper",
        #x=pos, y=1.05,
        #sizex=0.2, sizey=0.2,
        #xanchor="right", yanchor="bottom"
    #)
    #)
    # Se setea el zoom inicial:
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
    fig2.update_xaxes(type="date", range=[start_date, end_date])
    table1 = make_Mplanta_table(df1, df2)
    table2 = make_dataCen_table(df1)
    return fig1, fig2, table1, table2