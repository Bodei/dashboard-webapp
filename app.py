import dash
import dash_core_components as dcc
import dash_html_components as html
import time
import plotly.graph_objs as go
from collections import deque
import random
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash('Solar-Cooling-Dashboard', external_stylesheets=external_stylesheets)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

max_length = 100
times = deque(maxlen=max_length)
panel_temp = deque(maxlen=max_length)
solar_rad = deque(maxlen=max_length)
amb_temp = deque(maxlen=max_length)
humidity = deque(maxlen=max_length)

data_dict = {"Panel Temperature":panel_temp,
    "Solar Radiation":solar_rad,
    "Ambient Temperature":amb_temp,
    "Humidity":humidity}

# Dummy Data
def update_sensor_values(times, panel_temp, solar_rad, amb_temp, humidity):
    times.append(time.time())
    if len(times) == 1:
        # Starting relevant values
        panel_temp.append(random.randrange(60,120))
        solar_rad.append(random.randrange(1000,2000))
        amb_temp.append(random.randrange(30,100))
        humidity.append(random.randrange(10,100))
    else:
        for data_of_interest in [panel_temp, solar_rad, amb_temp, humidity]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))
    return times, panel_temp, solar_rad, amb_temp, humidity

times, panel_temp, solar_rad, amb_temp, humidity = update_sensor_values(times, panel_temp, solar_rad, amb_temp, humidity)

def serve_layout():
   return html.Div([
        html.Div([
            html.H2('Solar Cooling Data',
                style={'float': 'left',
                    }),
            ]),
        dcc.Dropdown(id='solar-data-name',
            options=[{'label': s, 'value': s}
                for s in data_dict.keys()],
            value=['Panel Temperature','Solar Radiation'],
            multi=True
            ),
        html.Div(children=html.Div(id='graphs'), className='row'),
        dcc.Interval(
            id='graph-update',
            interval=5000)
        ], className="container",style={'width':'98%','margin-left':10,'margin-right':10})

app.layout = serve_layout

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('solar-data-name','value')],
    events=[dash.dependencies.Event('graph-update','interval')]
    )

def update_graph(data_names):
    graphs = []
    global times
    global panel_temp
    global solar_rad
    global amb_temp
    global humidity
    times, panel_temp, solar_rad, amb_temp, humidity = update_sensor_values(times, panel_temp, solar_rad, amb_temp, humidity)
    
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'

    for data_name in data_names:
        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill='tozeroy',
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))
    return graphs

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})

if __name__ == '__main__':
    app.run_server(debug=True)
