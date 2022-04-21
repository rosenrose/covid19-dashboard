from dash import html


def make_table(df):
    return html.Table(
        children=[
            html.Thead(
                style={
                    "display": "block",
                    "paddingBottom": "1.5rem",
                },
                children=[
                    html.Tr(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "fontSize": "1rem",
                            "fontWeight": "600",
                        },
                        children=[
                            html.Th(column.replace("_", " ")) for column in df.columns
                        ],
                    )
                ],
            ),
            html.Tbody(
                style={
                    "display": "block",
                    "maxHeight": "50vh",
                    "overflow": "hidden scroll",
                },
                children=[
                    html.Tr(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "padding": "2rem 0",
                            "borderTop": "1px solid white",
                        },
                        children=[
                            html.Td(col, style={"textAlign": "center"}) for col in row
                        ],
                    )
                    for row in df.values
                ],
            ),
        ]
    )
