from ctypes import resize
import streamlit as st
import pandas as pd
import plotly.express as px
import sections


alert_container = st.empty()

st.markdown(
    """
# UK COP / IPOP Scholar Bot

Sponsored by University of Kentucky Institute for Pharmaceutical Outcomes and Policy.

This bot runs weekly to collect new Google Scholar data and email updated statistics to
anyone subscribed to the bot.

This project is open-source on [GitHub](https://github.com/UK-IPOP/scholar-bot).

"""
)


# sidebar section
sections.sidebar_content()


df = pd.read_csv("data/scholar_data.csv")

grouped = df.groupby("name").mean().reset_index()
top_20 = (
    grouped[["name", "cited_by"]]
    .sort_values(by="cited_by", ascending=False)
    .head(20)
    .sort_values(by="cited_by", ascending=True)
)

bar_chart = px.bar(
    top_20,
    x="cited_by",
    y="name",
    orientation="h",
    template="ggplot2",
    labels={"cited_by": "Citations", "name": "Name"},
).update_traces(marker_color="darkblue")

st.header("Leaderboard")
st.plotly_chart(bar_chart, use_container_width=True)


st.header("Author Citations Per Year")
selected_author = st.selectbox("Author Name:", df["name"].unique(), index=0)

author_table = df[df["name"] == selected_author]

with st.expander("Author Info"):
    row = author_table.iloc[0]
    st.json(
        {
            "Name": row["name"],
            "Affiliation": row["affiliation"],
            "hIndex": row["h_index"],
            "i10Index": row["i10_index"],
            "Publication Count": row["pub_count"],
            "Total Citations": row["cited_by"],
        }
    )
    st.markdown(
        f"""
    **Name**: {row["name"]}

    **Affiliation**: {row["affiliation"]}
    """
    )
    with st.container():
        stat1, stat2, stat3, stat4 = st.columns(4)
        # TODO: add changes (week) to stats
        stat1.metric(label="h-Index", value=int(row["h_index"]))
        stat2.metric(label="i10-Index", value=int(row["i10_index"]))
        stat3.metric(label="Publications", value=int(row["pub_count"]))
        stat4.metric(label="Citations", value=int(row["cited_by"]))


line_chart = (
    px.line(
        author_table,
        x="year",
        y="cites",
        template="ggplot2",
        labels={"cites": "Citations", "year": "Year"},
    )
    .update_yaxes(
        tick0=0,
    )
    .update_traces(line_color="darkblue")
)
st.plotly_chart(line_chart, use_container_width=True)


st.header("Raw Data Table")
st.markdown(
    "[Link to Data](https://github.com/UK-IPOP/scholar-bot/blob/main/data/scholar_data.csv)"
)
display_table = df[["name", "h_index", "i10_index", "pub_count", "cited_by"]]
display_table.columns = ["Name", "hIndex", "i10Index", "Publications", "Citations"]
display_table.drop_duplicates(inplace=True)
display_table.reset_index(drop=True, inplace=True)
st.dataframe(display_table)
