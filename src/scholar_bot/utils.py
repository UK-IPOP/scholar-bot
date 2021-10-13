from __future__ import annotations

import pandas as pd
import datetime


def load_data() -> pd.DataFrame:
    # replace w/ github eventually
    df = pd.read_csv("data/scholar_data.csv")
    df["day_added"] = pd.to_datetime(df.day_added)
    return df


def split_weekly_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    today = pd.to_datetime(datetime.date.today())
    df["day_diff"] = df.day_added.apply(lambda x: (today - x).days)

    today_data = df[df.day_added == today].copy()
    weekly_data = df[df.day_diff <= 7]
    return today_data, weekly_data


def get_metrics_change(author: str) -> dict[str, int]:
    metrics = ("h_index", "i10_index", "cited_by", "pub_count")
    df = load_data()
    today_data, weekly_data = split_weekly_data(df)
    data = {}
    data["name"] = author
    for metric in metrics:
        recent = today_data.groupby("name").mean()
        old = weekly_data.groupby("name").mean()
        data[metric] = recent.loc[author, metric] - old.loc[author, metric]
    return data


# example usage
# print(get_metrics_change("Adam Sieg"))
