from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]

app = Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "color": "white",
        "backgroundColor": "#333",
        "fontFamily": "Open Sans, sans-serif",
    },
    children=[
        html.Header(
            style={"paddingTop": "3rem"},
            children=[
                html.H1(
                    "COVID-19 Dashboard",
                    style={
                        "textAlign": "center",
                        "fontSize": "3rem",
                    },
                )
            ],
        )
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
