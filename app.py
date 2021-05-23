import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import markdown as md
import PIL as pil
from datetime import date
from pvlib import solarposition
import matplotlib.pyplot as plt
import io

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#4D4C4C',
    'color': 'white',
    'padding': '6px'
}

img1 = pil.Image.open(r'telebajski_sonce.jpg')

app.layout = html.Div([
    html.Div([
        dbc.Row([
            html.Img(
                src=img1,
                style={'display': 'inline-block', 'float': 'left',
                       'width': '240px', 'height': '130px', 'margin-top': '15px'}
            ),
            html.H1(
                'Motion of the sun simulator',
                style={'display': 'inline-block', 'float': 'right', 'margin': '0px 5px', 'color': 'white',
                       'margin-right': ' 80px'}
            ),
        ]),
dbc.Row([html.P('Authors: Primož Skledar, Jernej Vipavec, Zala Ferlic', style={'color': 'white'})]),
    ], style={
        'borderBottom': 'thin grey solid',
        'backgroundColor': '#3A3A3A',
        'padding': '10px 0px 10px 30px',
        'background-repeat': 'no-repeat',
        'background-size': 'cover'
    }),

    dcc.Tabs([
        dcc.Tab(label='App',
                children=[
                    html.Div([
                        html.Div([
                            html.H4('Insert data to plot diagram', style={'margin-left': '10px', 'color': 'white'}),
                            html.Div([
                                dbc.Row([
                                    html.P(
                                        'Latitude: ',
                                        style={'display': 'inline-block', 'float': 'left', 'margin': '14px 5px 0px 5px',
                                               'color': 'white'}
                                    ),
                                    dcc.Input(id="latitude", type="number",
                                              value=46.05,
                                              style={'display': 'inline-block', 'float': 'left',
                                                     'color': 'black'}),
                                    # html.P(
                                    #     ', 0',
                                    #     style={'display': 'inline-block', 'float': 'left', 'margin': '14px 5px 0px 5px',
                                    #            'color': 'white'}
                                    # ),
                                    # dcc.Input(id="longitude", type="number",
                                    #           value=14.50,
                                    #           style={'display': 'inline-block', 'float': 'left',
                                    #                  'color': 'black'}),
                                ])
                            ]),
                            html.Div([
                                dbc.Row([
                                    html.P(
                                        'Summer solstice',
                                        style={'display': 'inline-block', 'float': 'left', 'margin': '2% 5px 0px 5px',
                                               'color': 'white'}
                                    ),
                                    dcc.DatePickerSingle(
                                        id='date-single-picker-summer-solstice',
                                        date=date(2021, 6, 21),
                                        style={'display': 'inline-block', 'float': 'left', 'margin': '1% 5px 0px 5px',
                                               'color': 'white'}
                                    ), ]),
                                dbc.Row([
                                    html.P(
                                        'Spring equinox',
                                        style={'display': 'inline-block', 'float': 'left',
                                               'margin': '2% 5px 0px 5px',
                                               'color': 'white'}
                                    ),
                                    dcc.DatePickerSingle(
                                        id='date-single-picker-spring-equinox',
                                        date=date(2021, 3, 20),
                                        style={'display': 'inline-block', 'float': 'left',
                                               'margin': '1% 5px 0px 5px',
                                               'color': 'white'}
                                    ), ]),
                                dbc.Row([
                                    html.P(
                                        'Winter solstice',
                                        style={'display': 'inline-block', 'float': 'left',
                                               'margin': '2% 5px 0px 5px',
                                               'color': 'white'}
                                    ),
                                    dcc.DatePickerSingle(
                                        id='date-single-picker-winter-solstice',
                                        date=date(2021, 12, 21),
                                        style={'display': 'inline-block', 'float': 'left',
                                               'margin': '1% 5px 0px 5px',
                                               'color': 'white'}
                                    ),
                                ]),
                                dbc.Row([
                                    html.P(
                                        'Optional date',
                                        style={'display': 'inline-block', 'float': 'left',
                                               'margin': '2% 5px 0px 5px',
                                               'color': 'white'}
                                    ),
                                    dcc.DatePickerSingle(
                                        id='date-single-picker-optional',
                                        date=date(2021, 10, 28),
                                        style={'display': 'inline-block', 'float': 'left',
                                               'margin': '1% 5px 0px 5px',
                                               'color': 'white'}
                                    ),
                                ])

                            ]),
                            html.Div([
                                dbc.Row([
                                    html.P(
                                        'Start and end date of analemma',
                                        style={'display': 'inline-block', 'float': 'left', 'margin': '2% 5px 2% 5px',
                                               'color': 'white'}
                                    ),
                                    dcc.DatePickerSingle(
                                        id='date-single-picker-start',
                                        date=date(2021, 1, 1),
                                        style={'display': 'inline-block', 'float': 'left', 'margin': '1% 5px 1% 5px',
                                               'color': 'white'}
                                    ),
                                    dcc.DatePickerSingle(
                                        id='date-single-picker-end',
                                        date=date(2022, 1, 1),
                                        style={'display': 'inline-block', 'float': 'left', 'margin': '1% 5px 1% 5px',
                                               'color': 'white'}
                                    )

                                ])
                            ]),

                        ], style={'width': '48%', 'display': 'inline-block', 'float': 'left',
                                  'margin': '20px 20px 20px 20px',
                                  'borderBottom': 'thin lightgrey solid', 'backgroundColor': '#4D4C4C',
                                  'padding': '0px 0px 0px 0px', 'borderTop': 'thin lightgrey solid'}
                        )
                    ]),

                    html.Div([
                        html.Img(
                            id='plotted-graph',
                            style={'display': 'inline-block', 'float': 'right',
                                   'margin-top': '15px', 'margin-right': '15px'}
                        ),

                    ],
                        # style={
                        # 'position': 'relative',
                        # 'width': '40%', 'display': 'inline-block', 'float': 'right',
                        # 'borderTop': 'thin lightgrey solid',
                        # 'borderBottom': 'thin lightgrey solid',
                        # 'backgroundColor': '#B6B6B6',
                        # 'padding': '270px 0px -1px 0px',
                        # }
                    ),
                ], style=tab_style, selected_style=tab_selected_style),

        dcc.Tab(label='Table of examples', children=[
            html.Div(
                dbc.Row(
                    md.users_manual
                ), style={
                    'borderTop': 'thin lightgrey solid',
                    'borderBottom': 'thin lightgrey solid',
                    'backgroundColor': 'rgb(250, 250, 250)',
                    'padding': '10px 5px'}
            )], style=tab_style, selected_style=tab_selected_style)
    ]),
], style=tabs_styles)


def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    buf = io.BytesIO()
    fig.figure.savefig(buf)
    buf.seek(0)
    img = pil.Image.open(buf)
    return img


@app.callback(
    [Output('plotted-graph', 'src')],
    [Input('latitude', 'value'),
     # Input('longitude', 'value'),
     Input('date-single-picker-start', 'date'),
     Input('date-single-picker-end', 'date'),
     Input('date-single-picker-summer-solstice', 'date'),
     Input('date-single-picker-spring-equinox', 'date'),
     Input('date-single-picker-winter-solstice', 'date'),
     Input('date-single-picker-optional', 'date')])
def update_graph(lat, date_start, date_end, date_summer_solstice, date_spring_equinox, date_winter_solstice,
                 date_optional):
    times = pd.date_range(date_start, date_end, closed='left',
                          freq='H')
    lon = 0
    solpos = solarposition.get_solarposition(times, lat, lon)
    # remove nighttime
    solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

    ax = plt.subplot(1, 1, 1, projection='polar')
    # draw the analemma loops
    points = ax.scatter(np.radians(solpos.azimuth), solpos.apparent_zenith,
                        s=2, label=None, c=solpos.index.dayofyear)
    ax.figure.colorbar(points)

    # draw hour labels
    # for hour in np.unique(solpos.index.hour):
    #     # choose label position by the smallest radius for each hour
    #     subset = solpos.loc[solpos.index.hour == hour, :]
    #     r = subset.apparent_zenith
    #     pos = solpos.loc[r.idxmin(), :]
    #     ax.text(np.radians(pos['azimuth']), pos['apparent_zenith'], str(hour))

    # draw individual days
    for date in pd.to_datetime([date_summer_solstice, date_spring_equinox, date_winter_solstice, date_optional]):
        times = pd.date_range(date, date + pd.Timedelta('24h'), freq='5min')
        solpos = solarposition.get_solarposition(times, lat, lon)
        solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]
        label = date.strftime('%Y-%m-%d')
        ax.plot(np.radians(solpos.azimuth), solpos.apparent_zenith, label=label)

    ax.figure.legend(loc='upper left')

    # change coordinates to be like a compass
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rmax(90)

    image = fig2img(ax)
    return [image]


if __name__ == '__main__':
    app.run_server(debug=True)
