from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from data import countries_df, dropdown_options, make_time_series_df, make_totals_df
from builder import make_table
import json
import requests
from datetime import datetime
import base64
import io

# print(countries_df.values, dropdown_options)

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap",
]

app = Dash(__name__, external_stylesheets=stylesheets)
app.title = "COVID-19 Dashboard"

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

condition_colors = ["#e74c3c", "#8e44ad", "#27ae60"]

remote_daily_reports = json.loads(
    requests.get(
        "https://api.github.com/repos/CSSEGISandData/COVID-19/git/trees/master?recursive=1"
    ).text
)
daily_reports = [
    tree
    for tree in remote_daily_reports["tree"]
    if tree["path"].startswith("csse_covid_19_data/csse_covid_19_daily_reports/")
    and tree["path"].endswith(".csv")
]

for report in daily_reports:
    date = report["path"].split("/")[-1].split(".")[0]
    date = datetime.strptime(date, "%m-%d-%Y")
    date = f"{date:%Y-%m-%d}"
    report["date"] = date

daily_reports.sort(key=lambda x: x["date"], reverse=True)


def get_daily_report(date):
    for report in daily_reports:
        if report["date"] == date:
            return report


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
                "gridTemplateColumns": "60% 40%",
                "gap": "2rem",
                "marginBottom": "2rem",
            },
            children=[
                html.Div(dcc.Graph(figure=covid_map)),
                html.Div(make_table(countries_df)),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "20% 80%",
                "gap": "2rem",
            },
            children=[
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="daily-input",
                            options=[
                                {"label": report["date"], "value": report["date"]}
                                for report in daily_reports
                            ],
                            value=daily_reports[0]["date"],
                            style={
                                "width": "10rem",
                                "margin": "0 auto",
                                "color": "#333",
                            },
                        ),
                        dcc.Graph(id="totals-graph"),
                    ]
                ),
                html.Div(
                    children=[
                        # dcc.Input(placeholder="name?", id="hello-input"),
                        # html.H2("Hello Anonymous", id="hello-output"),
                        dcc.Dropdown(
                            id="country-input",
                            options=[
                                {"label": country, "value": country}
                                for country in dropdown_options
                            ],
                            value="global",
                            style={
                                "width": "20rem",
                                "margin": "0 auto",
                                "color": "#333",
                            },
                        ),
                        dcc.Graph(id="time-series-graph"),
                    ],
                ),
            ],
        ),
    ],
)
# @app.callback(Output("hello-output", "children"), [Input("hello-input", "value")])
# def update_hello(value):
#     return f"Hello {value if value else 'there'}"
@app.callback(Output("time-series-graph", "figure"), [Input("country-input", "value")])
def update_time_series(value):
    df = make_time_series_df(country=value)
    line_chart = px.line(
        df,
        x="date",
        y=df.columns[1:],
        labels={
            "date": "Date",
            "value": "Cases",
            "variable": "Condition",
        },
        hover_data={
            "value": ":,",
            "variable": False,
        },
        template="plotly_dark",
    )
    line_chart.update_xaxes(rangeslider_visible=True, showgrid=False)

    for i, data in enumerate(line_chart["data"]):
        data["line"]["color"] = condition_colors[i]

    return line_chart


@app.callback(Output("totals-graph", "figure"), [Input("daily-input", "value")])
def update_totals(value):
    report = get_daily_report(value)
    content = json.loads(requests.get(report["url"]).text)["content"]
    blob = base64.b64decode(content)

    bar_chart = px.bar(
        make_totals_df(io.BytesIO(blob)),
        title="Total Global Cases",
        x="condition",
        y="count",
        hover_data={"count": ":,", "condition": False},
        labels={"condition": "Condition", "count": "Cases"},
        template="plotly_dark",
    )
    # bar_chart.update_layout(xaxis={"title": "Condition"}, yaxis={"title": "Cases"})
    bar_chart.update_traces(marker_color=condition_colors)

    return bar_chart


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
