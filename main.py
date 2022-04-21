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

covid_map = px.scatter_geo(
    countries_df,
    title="Confirmed By Country",
    locations="Country_Region",
    locationmode="country names",
    color="Confirmed",
    color_continuous_scale=px.colors.sequential.Oryel,
    hover_name="Country_Region",
    hover_data={
        "Confirmed": ":,",
        "Deaths": ":,",
        "Recovered": ":,",
        "Country_Region": False,
    },
    size="Confirmed",
    size_max=40,
    projection="natural earth",
    template="plotly_dark",
)
covid_map.update_layout(margin={"l": 0, "r": 0, "t": 50, "b": 0})

bar_chart = px.bar(
    totals_df,
    title="Total Global Cases",
    x="condition",
    y="count",
    hover_data={"count": ":,", "condition": False},
    labels={"condition": "Condition", "count": "Cases"},
    template="plotly_dark",
)
# bar_chart.update_layout(xaxis={"title": "Condition"}, yaxis={"title": "Cases"})
bar_chart.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

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
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(8, 1fr)",
                "gap": "2rem",
            },
            children=[
                html.Div(dcc.Graph(figure=covid_map), style={"gridColumn": "span 5"}),
                html.Div(make_table(countries_df), style={"gridColumn": "span 3"}),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",
                "gap": "2rem",
            },
            children=[
                html.Div(dcc.Graph(figure=bar_chart), style={"gridColumn": "span 3"})
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
