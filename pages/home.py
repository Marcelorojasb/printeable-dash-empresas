import dash
import plotly.graph_objs as go
from datetime import date # Objetos 'date'
from dateutil.relativedelta import relativedelta
from dash import dcc, html, Input, Output, callback
from plotly.subplots import make_subplots # Múltiples plots en gráficos
from PIL import Image
from utils import make_Mplanta_table, make_dataCen_table, make_dataRet_table,  make_dataRes_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
#2.0
dash.register_page(__name__,path='/')

# Overview data
#df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
#df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))
emp_dict = pd.read_parquet(DATA_PATH.joinpath("cen_emp_dict.parquet"), engine='pyarrow')
casos_list = [[pd.read_parquet(DATA_PATH.joinpath("centrales.parquet"), engine='pyarrow'),''], 
              [pd.read_parquet(DATA_PATH.joinpath("centralesFCTA.parquet"), engine='pyarrow'),'ANDINA'],] # Nombre de la central en el plp
casos_listb = [[pd.read_parquet(DATA_PATH.joinpath("barras.parquet"), engine='pyarrow'),''], 
              [pd.read_parquet(DATA_PATH.joinpath("barrasFCTA.parquet"), engine='pyarrow'),'ANDINA']]
ret = {'Engie': pd.read_parquet(DATA_PATH.joinpath("engie_retiros.parquet"), engine='pyarrow')}
auxCBcen_df = casos_list[0][0]
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
end_dt = date(
    year=int(plpdate[0:4])+3,
    month=int(plpdate[5:7]),
    day=1
)

# store the dates between two dates in a list
dates = []
while start_date <= end_dt:
    # add current date to list by converting  it to iso format
    dates.append(start_date.isoformat())
    # increment start date by timedelta
    start_date += relativedelta(months=1)

#2.0
layout = html.Div(
        [
            # page 1
            html.Div(
                [
                    html.Div([
                        'Seleccione empresa',
                        dcc.Dropdown(id='Emp', options=emp_dict.loc['Empresa'].unique(), value=[emp_dict.loc['Empresa'].unique()[0]], clearable=False, multi=True), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione caso',
                        dcc.Dropdown(id='Caso', options=['caso base', 'falla CTA Engie'], value=['caso base'], clearable=False, multi=True), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione central',
                        dcc.Dropdown(id = 'Cen', value=auxCBcen_df['cen_nom'].unique()[0]), # Selección de la central (por nombre)
                    ], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Div([
                        'Seleccione simulación',
                        dcc.Dropdown(id='Sim', options=auxCBcen_df['Hidro'].unique(), value=auxCBcen_df['Hidro'].unique()[0], clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Div([
                        'Seleccione fecha de inicio',
                        dcc.Dropdown(id='init', options=dates, value=dates[0], clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Div([
                        'Seleccione fecha de termino',
                        dcc.Dropdown(id='end', options=dates, value=dates[12], clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([], className='no-print'),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(" Resumen Margen Planta y Contrato"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Ingresos vs costos por central. La generación no varía al producirse fallas. \
                                        El costo marginal de la barra varía al producirse fallas.",
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
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Datos Planta"], className="subtitle padded"
                                    ),
                                    html.Table(id='datos-planta-table'),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Ingresos/Costos",
                                        className="subtitle padded",
                                    ),
                                    html.Table(id='m-planta-table'),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "20px"},
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Tabla ingresos/costos"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Ingresos vs costos por central. La generación no varía al producirse fallas. \
                                        El costo marginal de la barra varía al producirse fallas.",
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
                                    html.H6("Ingresos planta", className="subtitle padded"),
                                    dcc.Graph(id="margen_planta",)
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
                    html.Div([
                        'Seleccione grupo',
                        dcc.Dropdown(id='gp', options=['Engie'], value='Engie', clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione barra (gráfico retiros por barra)',
                        dcc.Dropdown(id='Bar0', options=ret['Engie']['BarraPLP'].unique(), value='EntreRios220', clearable=False), # Selección de la simulación
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
                                    html.Table(id='datos-retiros-table0'),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6("Distribución de clientes", className="subtitle padded"),
                                    dcc.Graph(id="clientes0",)
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "20px"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Resumen"),
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
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        ["Tabla resumen"], className="subtitle padded"
                                    ),
                                    html.Table(id='resumen-table0'),
                                ],
                                className="six columns",
                            ),                       
                        ],
                        className="row",
                    ),
                ],
                className="letterpage",
            ),
            html.Div(
                [
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Valorizado por barra", className="subtitle padded"),
                                    dcc.Graph(id="val-bar0",)
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
    [Output(component_id='Cen',component_property='options'),
     Output(component_id='m-planta-table', component_property='children'),
    ],
    [Input(component_id='Emp',component_property='value'),
     Input(component_id='Caso',component_property='value'),
     Input(component_id='Sim',component_property='value'),
     Input(component_id='init',component_property='value'),
     Input(component_id='end',component_property='value')
    ])
def update_dropdown(empresa, caso, Sim, init, end):
    options = emp_dict.loc[:,emp_dict.loc['Empresa',:].isin(empresa)].columns
    options = options.values
    options = options.tolist()
    cen_casos = []
    fallas = []
    casos = []
    for id, i in enumerate(caso): # Se recorren lo plp si hay más de 1
        cen_falla = casos_list[id][1]
        perdidas_df = auxCBcen_df.loc[auxCBcen_df['cen_nom'].str.strip() == cen_falla]
        perdidas_df = perdidas_df.loc[perdidas_df['date']<=end]
        perdidas_df = perdidas_df.loc[perdidas_df['date']>=init]
        perdidas_df = perdidas_df.loc[perdidas_df['Hidro'].str.strip() == Sim.strip()]
        cenDP_df = casos_list[id][0]
        cenDP_df = cenDP_df.loc[cenDP_df['date']<=end]
        cenDP_df = cenDP_df.loc[cenDP_df['date']>=init] 
        df1DP = cenDP_df.loc[(cenDP_df['cen_nom'].str.strip()).isin(options)] # Se filtra por nombre de la central
        df1DP = df1DP.loc[df1DP['Hidro'].str.strip() == Sim.strip()]
        df1DP = df1DP.sort_values(by=['date']) # Se ordenan los datos por fecha para los gráficos de linea
        cen_casos.append(df1DP)
        fallas.append(perdidas_df)
        casos.append(i)
    table = make_Mplanta_table(cen_casos,fallas,casos)
    return options, table

@callback(
    [Output(component_id='margen_planta', component_property='figure'),
     Output(component_id='datos-planta-table', component_property='children')],
    [Input(component_id='Caso',component_property='value'),
     Input(component_id='Cen', component_property='value'), # Central seleccionada
     Input(component_id='Sim',component_property='value'),
     Input(component_id='init',component_property='value'),
     Input(component_id='end',component_property='value')])
def update_planta(caso,Cen,Sim,init,end):
    # Margen planta
    start_date = init
    end_date = end
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    for id, i in enumerate(caso): # Se recorren lo plp si hay más de 1
        cen_df = casos_list[id][0]
        df1 = cen_df.loc[cen_df['cen_nom'].str.strip() == Cen.strip()] # Se filtra por nombre de la central
        df1 = df1.loc[df1['Hidro'].str.strip() == Sim.strip()]
        df1 = df1.sort_values(by=['date']) # Se ordenan los datos por fecha para los gráficos de linea
        fig1.add_trace(
            go.Bar(x=df1['date'], y=df1['CenPgen'], name="P generada " + i + " [MW]"),
            secondary_y=False,
        )
        # Costo marginal de la barra (se muestra el de la primera fecha en la lista):
        fig1.add_trace(
            go.Scatter(x=df1['date'], y=df1['CMgBar'], name="Cmg barra "+ i + "[USD|MWh]"),
            secondary_y=True,
        )
        # Ingreso unitario:
        fig1.add_trace(
            go.Scatter(x=df1['date'], y=df1['iu'], name="Ingreso unitario " + i + "[USD|MWh]"),
            secondary_y=True,
        )
    # Se crea el primer gráfico (Generación/CMG/ingreso unitario): 
    # Gráfico de barra de potencia generada
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
    # Título del eje x:
    table1 = make_dataCen_table(df1)
    return fig1, table1


@callback(
    [Output(component_id='clientes0', component_property='figure'),
     Output(component_id='datos-retiros-table0', component_property='children')],
    [Input(component_id='gp',component_property='value'),
     Input(component_id='Caso', component_property='value')])
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
        val_acum.append((sum(val_mes),i))
    table = make_dataRet_table(max_client, val_acum, emp)
    return fig1, table

@callback(
    Output(component_id='val-bar0', component_property='figure'),
    [Input(component_id='gp',component_property='value'),
     Input(component_id='Caso', component_property='value'),
     Input(component_id='Bar0',component_property='value')])
def update_bar(emp,casos,bar):
    process_df = ret[emp]
    process_df = process_df.loc[process_df['Tipo']!='T'] #*****
    # Gráfico año mes
    añomesbar_df=process_df.groupby(['BarraPLP','Clave Año_Mes'], as_index=False)[['Medida_kWh']].sum()
    añomesbar_df['Clave Año_Mes'] = '20' + añomesbar_df['Clave Año_Mes'].astype(str)
    añomesbar_df['Clave Año_Mes'] = pd.to_datetime(añomesbar_df['Clave Año_Mes'], format='%Y%m')
    barfig_df = añomesbar_df.loc[añomesbar_df['BarraPLP'].str.strip()==bar.strip()]
    init1 = date(
    year=2024,
    month=1,
    day=1)
    end1 = date(
    year=2024,
    month=12,
    day=1)
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    for id, i in enumerate(casos):
        # Gráfico año mes barra
        bar_df = casos_listb[id][0]
        bar_df = bar_df.loc[bar_df['Hidro'].str.strip() == 'MEDIA']
        df1 = bar_df.loc[bar_df['bar_nom'].str.strip() == bar.strip()] # Se filtra por nombre de la central
        df1 = df1.loc[df1['date'].dt.date <= end1]
        df1 = df1.loc[df1['date'].dt.date >= init1]
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
    return fig4

@callback(
     Output(component_id='resumen-table0', component_property='children'),
    [Input(component_id='Emp',component_property='value'),
     Input(component_id='Sim',component_property='value'),
     Input(component_id='init',component_property='value'),
     Input(component_id='end',component_property='value'),
     Input(component_id='gp',component_property='value'),
     Input(component_id='Caso', component_property='value')])
def update_resumen(empresa, Sim, init, end, emp, caso):
    options = emp_dict.loc[:,emp_dict.loc['Empresa',:].isin(empresa)].columns
    options = options.values
    options = options.tolist()
    cen_casos = []
    casos = []
    for id, i in enumerate(caso): # Se recorren lo plp si hay más de 1
        cenDP_df = casos_list[id][0]
        cenDP_df = cenDP_df.loc[cenDP_df['date']<=end]
        cenDP_df = cenDP_df.loc[cenDP_df['date']>=init] 
        df1DP = cenDP_df.loc[(cenDP_df['cen_nom'].str.strip()).isin(options)] # Se filtra por nombre de la central
        df1DP = df1DP.loc[df1DP['Hidro'].str.strip() == Sim.strip()]
        df1DP = df1DP.sort_values(by=['date']) # Se ordenan los datos por fecha para los gráficos de linea
        cen_casos.append(df1DP)
        casos.append(i)
    process_df = ret[emp]
    process_df = process_df.loc[process_df['Tipo']!='T'] #*****
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
    for id, i in enumerate(caso):
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
        val_acum.append((sum(val_mes),i))
    table = make_dataRes_table(cen_casos,casos, val_acum, emp)
    return table