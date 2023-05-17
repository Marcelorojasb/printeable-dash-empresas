import dash
from dash import dcc, html

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()], className='no-print')


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url("Marca/marca_sin_bajada.png"),
                            className="logo",
                        ),
                        href="/",
                    ),
                    #html.A(
                        #html.Button(
                            #"Enterprise Demo",
                            #id="learn-more-button",
                            #style={"margin-left": "-10px"},
                        #),
                        #href="https://plotly.com/get-demo/",
                    #),
                    #html.A(
                        #html.Button("Source Code", id="learn-more-button"),
                        #href="https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-financial-report",
                    #),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.H5("Margen Planta - Contrato"),
                    #html.Div(
                        #[
                            #dcc.Link(
                                #"Full View",
                                #href="/dash-financial-report/full-view",
                                #className="full-view-link",
                            #)
                        #],
                        #className="five columns",
                    #),
                ],
                className="twelve columns main-title",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Resumen",
                href="/resumen",
                className="tab first",
            ),
            dcc.Link(
                "Margen Planta",
                href="/margen-planta",
                className="tab",
            ),
            dcc.Link(
                "Margen Contrato",
                href="/margen-contrato",
                className="tab",
            ),
            dcc.Link(
                "Tablas", href="/tablas", className="tab"
            ),
            dcc.Link(
                "Distribución",
                href="/distribucion",
                className="tab",
            ),
            dcc.Link(
                "Contacto",
                href="/contacto",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

def make_Mplanta_table(cen_df, bar_df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    ingresos = bar_df['CMgBar'].values*cen_df['CenPgen'].values
    ingresos = str(round(sum(ingresos),2)) + '   [USD/año]'
    costos = cen_df['CenCVar'].values*cen_df['CenPgen'].values
    costos = str(round(sum(costos),2)) + '   [USD/año]'
    row_c = [html.Td("Costos"), html.Td(costos)]
    row_i = [html.Td("Ingresos "), html.Td(ingresos)]
    return [html.Tr(row_c), html.Tr(row_i)]


def make_dataCen_table(cen_df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    cen_nom = cen_df['cen_nom'].unique()[0]
    cen_num = cen_df['cen_num'].unique()[0]
    tipo = cen_df['tipo'].unique()[0]
    bar_nom = cen_df['bar_nom'].unique()[0]
    plp_date = cen_df['plp_date'].unique()[0]
    row_cnom = [html.Td("Central"), html.Td(cen_nom)]
    row_cnum = [html.Td("Número"), html.Td(cen_num)]
    row_tipo = [html.Td("Tipo"), html.Td(tipo)]
    row_bnom = [html.Td("Barra"), html.Td(bar_nom)]
    row_date = [html.Td("Fecha datos"), html.Td(plp_date[5:7]+'/'+ plp_date[0:4])]
    return [html.Tr(row_cnom), html.Tr(row_cnum), html.Tr(row_tipo), html.Tr(row_bnom), html.Tr(row_date)]