import json
import dash
import dash_leaflet as dl
import dash_html_components as html
from dash.dependencies import Input, Output, ALL

# Setup markers.
locations = [[40, -4], [40, -4.5], [40.5, -4], [40.5, -4.5]]
markers = [dl.Marker(position=l, id=dict(id=i)) for i, l in enumerate(locations)]
# Create small example dash app showing a map and a div (for logging).
app = dash.Dash(prevent_initial_callbacks=True)
app.layout = html.Div([
    dl.Map([dl.TileLayer()] + markers, center=[40.25, -4.25], zoom=14,
           style={'width': '1000px', 'height': '500px'}),
    html.Div(id="log")
])

# Callback for interactivity.
@app.callback(Output("log", "children"), Input(dict(id=ALL), "n_clicks"))
def log_position(_):
    idx = json.loads(dash.callback_context.triggered[0]['prop_id'].split(".")[0])["id"]
    location = locations[idx]
    print(location)  # print location to console
    return location  # print location to ui

if __name__ == '__main__':
    app.run_server()