from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import html

# layout for the login page
# Define the layout for the login page
login_layout = html.Div([
    # Header with logo and title
    html.Div([
        html.Img(src='/assets/logo.png', style={'width': '150px', 'height': 'auto', 'marginBottom': '20px'}),
        html.H1("EcoMol Lab", style={'color': '#007bff'})
    ], className='login-header'),

    # Main login form container
    html.Div([
        html.H2("Login", style={'marginBottom': '20px', 'color': '#333'}),
        dcc.Input(id='username-input', type='text', placeholder='Username', className='login-input'),
        dcc.Input(id='password-input', type='password', placeholder='Password', className='login-input'),
        html.Button('Login', id='login-button', n_clicks=0, className='login-button'),
        html.Div(id='login-output', className='login-output')
    ], className='login-form'),

    # Footer
    html.Div("© 2023 HABER Solutions - All rights reserved", className='login-footer')
], className='login-container')



layout = html.Div([
    html.Header([
        html.Img(src='/assets/logo.png', className='logo', style={'width': '100px', 'height': 'auto'}),  # Logo or Image for branding
        html.H1("EcoMol Lab", className="header-title")
    ],
    style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'},
    className="app-header"),
    
    # Body
    html.Div([
        html.Div([
            # Ketcher editor
            html.Iframe(
                id='ketcher-frame',
                src='/assets/standalone/index.html',
                style={'width': '80%', 'height': '500px', 'border': '1px solid #ccc', 'margin-bottom': '20px'}
            ),

            # Settings options and Dropdown container
            html.Div([
                # Settings options
                html.Div([
                    html.Div([
                        html.Label('Number of Tries:', htmlFor='n_tries'),
                        dcc.Input(id='n_tries', type='number', value=5, className='input-style')
                    ], className='input-container'),

                    html.Div([
                        html.Label('Population Size:', htmlFor='population_size'),
                        dcc.Input(id='population_size', type='number', value=5, className='input-style')
                    ], className='input-container'),

                    html.Div([
                        html.Label('Mating Pool Size:', htmlFor='mating_pool_size'),
                        dcc.Input(id='mating_pool_size', type='number', value=20, className='input-style')
                    ], className='input-container'),

                    html.Div([
                        html.Label('Generations:', htmlFor='generations'),
                        dcc.Input(id='generations', type='number', value=2, className='input-style')
                    ], className='input-container'),

                    html.Div([
                        html.Label('Mutation Rate:', htmlFor='mutation_rate'),
                        dcc.Input(id='mutation_rate', type='number', value=0.05, className='input-style')
                    ], className='input-container')
                ], className='settings-container', style={'width': '50%', 'display': 'inline-block'}),

                # Dropdown
                html.Div([
                    dcc.Dropdown(
                        id='design-category-dropdown',
                        options=[
                            {'label': 'API Unit Cleaning Agent', 'value': 'api_unit_cleaning_agent'},
                            {'label': 'Chemical Compound Purification', 'value': 'chemical_purification'},
                            {'label': 'API Production & Isolation', 'value': 'api_production_purification'}
                        ],
                        placeholder="Select a Design Template",
                        className='dropdown-style'
                    ),

                    # Section for displaying pictures
                    html.Div(
                        id='category-images-container',
                        children=[],
                        style={'display': 'none', 'justifyContent': 'center', 'alignItems': 'center', 'marginBottom': '50px'}
                    )
                ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            ], style={'display': 'flex', 'justifyContent': 'center'}),

            # Run design button
            html.Button('Run Design', id='run-design-button', className="button-run-design")
        ], className="editor-and-settings-container")
    ], className="editor-container", id="editor-container", style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-top': '20px'}),

    # Output for results (initially hidden)
     html.Div(
        id='molecule-output-container',
        children=[
            # Plot Section
            dcc.Graph(
                id='molecule-plot',
                style={'width': '100%', 'textAlign': 'center'}
            ),

            # Molecule Properties Table
            html.Div(
                id='molecule-properties-table',
                className='molecule-properties',
                style={'width': '100%', 'marginTop': '20px'}  # Full width for the table, with some margin at the top
            )
        ],
        style={'display': 'none'}
    ),

    html.Footer("© 2023 HABER Solutions - All rights reserved", className="app-footer")
], className="app-container")