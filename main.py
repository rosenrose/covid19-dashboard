import pandas as pd

def make_global_df(condition):
    df = pd.read_csv(f"data/time_series_{condition}.csv")
    df = df.drop(columns=["Province/State", "Country/Region", "Lat", "Long"])
    # df = df.iloc[:, :561]
    df = df.sum().reset_index(name=condition)
    df = df.rename(columns={"index": "date"})
    return df

daily_dataframe = pd.read_csv("data/daily_report_2021-03-06.csv")

totals_df = daily_dataframe[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
totals_df = totals_df.rename(columns={"index": "condition"})

countries_df = daily_dataframe[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries_df = countries_df.groupby("Country_Region").sum().reset_index()

conditions = ["confirmed", "deaths", "recovered"]
final_df = None

for condition in conditions:
    condition_df = make_global_df(condition)
    if final_df is None:
        final_df = condition_df
    else:
        final_df = final_df.merge(condition_df)
