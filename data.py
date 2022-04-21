import pandas as pd


def make_condition_df(condition, country=None):
    df = pd.read_csv(f"data/time_series_{condition}.csv")

    if country:
        df = df.loc[df["Country/Region"] == country]

    df = df.drop(columns=["Province/State", "Country/Region", "Lat", "Long"]).sum()
    # df = df.iloc[:, :561]
    df = df.reset_index(name=condition).rename(columns={"index": "date"})
    return df


def make_df(country=None):
    final_df = None
    for condition in conditions:
        condition_df = make_condition_df(condition, country)

        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)

    return final_df


daily_dataframe = pd.read_csv("data/daily_report_2021-03-06.csv")
# daily_dataframe = pd.read_csv("data/daily_report_2022-04-19.csv")

totals_df = daily_dataframe[["Confirmed", "Deaths", "Recovered"]].sum()
totals_df = totals_df.reset_index(name="count").rename(columns={"index": "condition"})

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

conditions = ["confirmed", "deaths", "recovered"]

global_df = make_df()

if __name__ == "__main__":
    print(totals_df)
    print(countries_df)
    print(global_df)
    print(make_df("Korea, South"))
