import dash
import plotly.graph_objs as go
from datetime import date # Objetos 'date'
from dash import dcc, html, Input, Output, callback
from plotly.subplots import make_subplots # Múltiples plots en gráficos
from PIL import Image
from utils import make_dataRet_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
#2.0
dash.register_page(__name__,path='/margen-contrato')

# Overview data
#df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
#df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))
casos_listb = [[pd.read_parquet(DATA_PATH.joinpath("barras.parquet"), engine='pyarrow'),''], 
              [pd.read_parquet(DATA_PATH.joinpath("barrasFCTA.parquet"), engine='pyarrow'),'ANDINA']]
emp_dict = pd.read_parquet(DATA_PATH.joinpath("cen_emp_dict.parquet"), engine='pyarrow')
ret = {'Engie': pd.read_parquet(DATA_PATH.joinpath("engie_retiros.parquet"), engine='pyarrow')}
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
                        dcc.Dropdown(id='Emp3', options=['Engie'], value='Engie', clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione caso',
                        dcc.Dropdown(id='Caso3', options=['Caso base', 'Caso falla FCTA'], value=['Caso base'], clearable=False, multi=True), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione barra (gráfico retiros por barra)',
                        dcc.Dropdown(id='Bar', options=ret['Engie']['BarraPLP'].unique(), value='EntreRios220', clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Margen contrato"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Ingresos/Costos (o tarifas) a partir de los retiros del grupo o empresa (casos base o falla), \
                                    considerar fallas genera cambios en los costos marginales y por tanto también en los ingresos, \
                                    costos y tarifas.\
                                    En la tabla 'Datos retiro', puede observar el mayor retiro de la empresa seleccionada y el total \
                                    recaudado por retiros (valorizado total) en cada caso (caso predeterminado caso base).",
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
                                        ["Datos Retiros"], className="subtitle padded"
                                    ),
                                    html.Table(id='datos-retiros-table'),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6("Distribución de clientes", className="subtitle padded"),
                                    dcc.Graph(id="clientes",)
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
                                    html.H6("Valorizado por barra", className="subtitle padded"),
                                    dcc.Graph(id="val-bar",)
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                ],
                className="letterpage",
            ),
            html.Div(
                [
                    # Row 6
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Valorizado total por mes", className="subtitle padded"),
                                    dcc.Graph(id="mgc",)
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),

                    # Row 7
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Retiros por mes", className="subtitle padded"),
                                    dcc.Graph(id="ret-mes",)
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
    [Output(component_id='clientes', component_property='figure'),
     Output(component_id='mgc', component_property='figure'),
     Output(component_id='datos-retiros-table', component_property='children')],
    [Input(component_id='Emp3',component_property='value'),
     Input(component_id='Caso3', component_property='value')])
def update_contrato(emp,casos):
    process_df = ret[emp]
    process_df = process_df.loc[process_df['Tipo']!='T'] #*****
    clientes_df=process_df.groupby(['Retiro'], as_index=False)['Medida_kWh'].sum()
    labels = clientes_df['Retiro'].values
    labels = labels.tolist()
    values = abs(clientes_df['Medida_kWh'].values)
    values = values.tolist()
    max_id = values.index(max(values))
    max_client = (labels[max_id],values[max_id])
    fig1 = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig1.update_traces(textposition='inside')
    fig1.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
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
    fig1.update(layout_showlegend=False)
    añomesbar_df=process_df.groupby(['BarraPLP','Clave Año_Mes'], as_index=False)[['Medida_kWh']].sum()
    añomesbar_df['Clave Año_Mes'] = '20' + añomesbar_df['Clave Año_Mes'].astype(str)
    añomesbar_df['Clave Año_Mes'] = pd.to_datetime(añomesbar_df['Clave Año_Mes'], format='%Y%m')
    init = date(
    year=2024,
    month=1,
    day=1)
    end = date(
    year=2024,
    month=12,
    day=1)
    val_acum = []
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    for id, i in enumerate(casos):
        bar_df = casos_listb[id][0]
        bar_df = bar_df.loc[bar_df['Hidro'].str.strip() == 'MEDIA']
        bar_df = bar_df.loc[bar_df['date'].dt.date <= end]
        bar_df = bar_df.loc[bar_df['date'].dt.date >= init]
        val_mes = 0
        for bar in añomesbar_df['BarraPLP'].unique():
            df1 = bar_df.loc[bar_df['bar_nom'].str.strip() == bar.strip()]
            df1 = df1.sort_values(by=['date'])
            barfig_df = añomesbar_df.loc[añomesbar_df['BarraPLP'].str.strip() == bar.strip()]
            val_mes = -barfig_df['Medida_kWh'].values*df1['CMgBar'].values/1000 + val_mes
        fig3.add_trace(
            go.Bar(x=barfig_df['Clave Año_Mes'], y=val_mes, name="Valorizado total" + i +  " [USD]"),
            secondary_y=False,)
        val_acum.append((sum(val_mes),i))
    fig3.update_xaxes(title_text="Fecha")
    # Título del eje y principal:
    fig3.update_yaxes(title_text="[USD]", secondary_y=False)
    fig3.update_layout(legend=dict(
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
    table = make_dataRet_table(max_client, val_acum, emp)
    return fig1, fig3, table

@callback(
    [Output(component_id='val-bar', component_property='figure'),
     Output(component_id='ret-mes', component_property='figure')],
    [Input(component_id='Emp3',component_property='value'),
     Input(component_id='Caso3', component_property='value'),
     Input(component_id='Bar',component_property='value')])
def update_bar(emp,casos,bar):
    process_df = ret[emp]
    process_df = process_df.loc[process_df['Tipo']!='T'] #*****
    añomes_df=process_df.groupby(['Clave Año_Mes'], as_index=False)[['Medida_kWh']].sum() 
    añomes_df['Clave Año_Mes'] = '20' + añomes_df['Clave Año_Mes'].astype(str)
    añomes_df['Clave Año_Mes'] = pd.to_datetime(añomes_df['Clave Año_Mes'], format='%Y%m')
    # Gráfico año mes
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
        go.Bar(x=añomes_df['Clave Año_Mes'], y=-añomes_df['Medida_kWh'], name="Retiros por mes " +  " [kWh]"),
        secondary_y=False,)
    fig2.update_xaxes(title_text="Fecha")
    # Título del eje y principal:
    fig2.update_yaxes(title_text="[kWh]", secondary_y=False)
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
    añomesbar_df=process_df.groupby(['BarraPLP','Clave Año_Mes'], as_index=False)[['Medida_kWh']].sum()
    añomesbar_df['Clave Año_Mes'] = '20' + añomesbar_df['Clave Año_Mes'].astype(str)
    añomesbar_df['Clave Año_Mes'] = pd.to_datetime(añomesbar_df['Clave Año_Mes'], format='%Y%m')
    barfig_df = añomesbar_df.loc[añomesbar_df['BarraPLP'].str.strip()==bar.strip()]
    init = date(
    year=2024,
    month=1,
    day=1)
    end = date(
    year=2024,
    month=12,
    day=1)
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    for id, i in enumerate(casos):
        # Gráfico año mes barra
        bar_df = casos_listb[id][0]
        bar_df = bar_df.loc[bar_df['Hidro'].str.strip() == 'MEDIA']
        df1 = bar_df.loc[bar_df['bar_nom'].str.strip() == bar.strip()] # Se filtra por nombre de la central
        df1 = df1.loc[df1['date'].dt.date <= end]
        df1 = df1.loc[df1['date'].dt.date >= init]
        df1 = df1.sort_values(by=['date']) # Se ordenan los datos por fecha para los gráficos de linea
        fig4.add_trace(
            go.Bar(x=barfig_df['Clave Año_Mes'], y=-barfig_df['Medida_kWh'].values*df1['CMgBar'].values/1000, name="Valorizado " + i +  " [USD]"),
            secondary_y=False,)
    fig4.update_xaxes(title_text="Fecha")
    # Título del eje y principal:
    fig4.update_yaxes(title_text="[USD]", secondary_y=False)
    fig4.update_layout(legend=dict(
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
    return fig4, fig2
        