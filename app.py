import os

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash('Solar-Cooling-Dashboard', external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([

    html.Div([
        html.H2("Solar Cooling Dashboard"),
    ],className='banner'),

    html.Div([
        html.P('The start of the dashboard for senior design project.'),
        html.P('Lots of work to go....')
    ])

],
className="row",
style={"margin": "0%"},
)

if __name__ == '__main__':
    app.run_server(debug=True)
