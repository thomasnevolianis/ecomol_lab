
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from backend.calculations import process_results
import plotly.express as px
from frontend.utils import smiles_to_image
from frontend.utils import get_color_for_property
from assets.credentials import USERS


def register_callbacks(app):
    @app.callback(
        Output('login-output', 'children'),
        Input('login-button', 'n_clicks'),
        State('username-input', 'value'),
        State('password-input', 'value')
    )
    def login_auth(n_clicks, username, password):
        if n_clicks > 0:
            if username in USERS and USERS[username] == password:
                return dcc.Location(id='redirect', pathname='/main')
            else:
                return 'Invalid username or password'
    @app.callback(
    Output('category-images-container', 'children'),
    Output('category-images-container', 'style'),
    Input('design-category-dropdown', 'value')
    )
    def update_image_container(selected_category):
        if not selected_category:
            return [], {'display': 'none'}

        # List of image file names for the selected category
        image_files = {
            'api_unit_cleaning_agent': ['/assets/3.png'],
            'chemical_purification': ['/assets/2.png'],
            'api_production_purification': ['/assets/1.png']
        }.get(selected_category, [])

        # Create html.Img components for each image
        images = [html.Img(src=f'{file}', style={'maxWidth': '80%', 'maxHeight': '150px'}) for file in image_files]

        return images, {'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginTop': '20px'}
    @app.callback(
        [Output('editor-container', 'style'),
         Output('molecule-output-container', 'style')],
        Input('run-design-button', 'n_clicks')
    )
    def toggle_visibility(n_clicks):
        if n_clicks and n_clicks > 0:
            return {'display': 'none'}, {'display': 'flex'}
        return {'display': 'block'}, {'display': 'none'}

    @app.callback(
        [Output('molecule-properties-table', 'children'),
         Output('molecule-plot', 'figure')],
        Input('run-design-button', 'n_clicks')
    )
    def update_output(n_clicks):
        if n_clicks and n_clicks > 0:
            molecules = process_results()
            sorted_molecules = sorted(molecules, key=lambda x: x['solubility'], reverse=True)

            table_content = [html.Tr([
                html.Th("Structure"),
                html.Th("SMILES"),
                html.Th("Solubility"),
                html.Th("Score"),
                html.Th("Reactivity"),
                html.Th("SA"),
                html.Th("CAS"),
                html.Th("Price (€)"),
                html.Th("CO2/kg"),
                html.Th("Overall")
            ])]
            for mol in sorted_molecules:
                image_src = smiles_to_image(mol["smiles"])
                image_html = html.Img(src=image_src, style={'width': '100px', 'height': '100px'})

                categories = ['Solubility', 'Score', 'Price (€)', 'CO2/kg']
                values = [mol['solubility'], mol['score'], mol['price_euro'], mol['co2_kg']]
                fig = px.line_polar(r=values, theta=categories, line_close=True)
                fig.update_traces(fill='toself', line=dict(width=2))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, max(values) + 0.5]),
                    ),
                    showlegend=False,
                    autosize=True,
                    margin=dict(l=20, r=20, t=20, b=20)
                )

                spider_chart = dcc.Graph(figure=fig, style={"width": "100%", "height": "100%"})

                row = html.Tr([
                    html.Td(image_html, style={'text-align': 'center'}),
                    html.Td(mol["smiles"]),
                    html.Td(mol["solubility"], style={'background-color': get_color_for_property(mol["solubility"])}),
                    html.Td(mol["score"], style={'background-color': get_color_for_property(mol["score"], False)}),
                    html.Td(mol["reactivity"]),
                    html.Td(mol["synthetic_accessibility"]),
                    html.Td(mol["cas"]),
                    html.Td(mol["price_euro"], style={'background-color': get_color_for_property(mol["price_euro"])}),
                    html.Td(mol["co2_kg"], style={'background-color': get_color_for_property(mol["co2_kg"])}),
                    html.Td(spider_chart, style={'text-align': 'center'})
                ])
                table_content.append(row)

            properties_table = html.Table(table_content)

            data = [go.Bar(x=[mol['smiles'] for mol in sorted_molecules], y=[mol['score'] for mol in sorted_molecules])]
            plot_layout = go.Layout(
                title="Molecule Scores",
                xaxis=dict(title='Molecules (SMILES)'),
                yaxis=dict(title='Score'),
                margin=dict(l=40, r=40, t=40, b=40),
                autosize=False,
                width=800,
                height=400
            )
            plot_figure = {'data': data, 'layout': plot_layout}

            return properties_table, plot_figure

        return [], {}

