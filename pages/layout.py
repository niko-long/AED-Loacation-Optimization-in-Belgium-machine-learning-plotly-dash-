import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def create_top_bar(title):
    return html.Div(
        style={
            'backgroundColor': '#1C4E80', 
            'color': 'white', 
            'padding': '10px 0', 
            'display': 'flex', 
            'justifyContent': 'center',
            'alignItems': 'center',
            'width': '100%',
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'zIndex': '1000',
            'margin': '0',
            'boxSizing': 'border-box'
        },
        children=[
            html.Div(
                children=[
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Home", href="http://localhost:8051"),
                            dbc.DropdownMenuItem("Map", href="http://localhost:8050"),
                            dbc.DropdownMenuItem("Page1", href="http://localhost:8053"),
                            dbc.DropdownMenuItem("Page2", href="http://localhost:8052")
                        ],
                        nav=True,
                        in_navbar=True,
                        label=html.Img(src='/assets/logo.png', height="40px", width="40px")
                    ),
                ],
                style={'position': 'absolute', 'left': '20px'}
            ),
            html.Div(
                style={'fontSize': '30px', 'fontWeight': 'bold'},
                children=title
            ),
            html.Div(
                style={'fontSize': '20px', 'position': 'absolute', 'right': '25px'},
                children='Group of CHINA'
            )
        ]
    )


# Placeholder to push content below fixed header
placeholder = html.Div(style={'height': '70px'})


if __name__ == '__main__':
    app.run_server(debug=True)
