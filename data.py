import pandas as pd
import requests
import json
from datetime import datetime
import base64
import io


def make_condition_df(condition, country):
    url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_{condition}_global.csv"
    df = pd.read_csv(url)

    if country != "global":
        df = df.loc[df["Country/Region"] == country]

    df = df.drop(columns=["Province/State", "Country/Region", "Lat", "Long"]).sum()
    # df = df.iloc[:, :561]
    df = df.reset_index(name=condition).rename(columns={"index": "date"})
    return df


def make_time_series_df(country):
    final_df = None
    for condition in conditions:
        condition_df = make_condition_df(condition, country)

        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)

    return final_df


def make_totals_df(csv):
    daily_dataframe = pd.read_csv(csv)
    totals_df = daily_dataframe[["Confirmed", "Deaths", "Recovered"]].sum()
    totals_df = totals_df.reset_index(name="count").rename(
        columns={"index": "condition"}
    )

    return totals_df


def get_csv_from_report(report):
    content = json.loads(requests.get(report["url"]).text)["content"]
    blob = base64.b64decode(content)
    return io.BytesIO(blob)


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

daily_dataframe = pd.read_csv(get_csv_from_report(daily_reports[0]))

countries_df = daily_dataframe[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries_df = (
    countries_df.groupby("Country_Region")
    .sum()
    .sort_values(by="Confirmed", ascending=False)
)
countries_df = countries_df.reset_index()

dropdown_options = countries_df.sort_values("Country_Region").reset_index()[
    "Country_Region"
]
dropdown_options = ["global", *dropdown_options]

conditions = ["confirmed", "deaths", "recovered"]

global_df = make_time_series_df("global")

if __name__ == "__main__":
    print(countries_df)
    print(global_df)
    print(make_time_series_df("Korea, South"))
