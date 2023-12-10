from dash import Dash
from frontend.layout import layout
from frontend.callbacks import register_callbacks
from frontend.layout import layout, login_layout
from dash.dependencies import Input, Output, State
from dash import dcc, html

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)
app.title = 'EcoMol Lab'

# URL Routing Callback
@app.callback(
    Output('app-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/main':
        return layout  # The main app layout
    else:
        return login_layout  # The login layout

# Set the initial layout to include URL routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='app-content')
])

# Register the callbacks
register_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)