from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from data import totals_df, countries_df, global_df
from builder import make_table

# print(countries_df.values)

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap",
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
            style={"paddingTop": "3rem", "marginBottom": "6rem"},
            children=[
                html.H1(
                    "COVID-19 Dashboard",
                    style={
                        "textAlign": "center",
                        "fontSize": "2.5rem",
                    },
                )
            ],
        ),
        html.Div(
            style={"display": "flex"},
            children=[
                html.Div(),
                html.Div(style={"width": "50%"}, children=[make_table(countries_df)]),
            ],
        ),
    ],
)

map_figure = px.scatter_geo(countries_df, projection="natural earth")
map_figure.show()

if __name__ == "__main__":
    app.run_server(debug=True)
