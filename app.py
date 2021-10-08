import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown(
    """
# UK IPOP Scholar Bot

Sponsored by University of Kentucky Institute for Pharmaceutical Outcomes and Policy.

This bot runs weekly to collect new Google Scholar data and email updated statistics to anyone subscribed to the bot.

"""
)

col1, col2 = st.columns(2)

with col1:
    st.image("assets/UK-COP-logo.jpg")


with col2:
    st.image("assets/IPOP-logo.png")


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


st.header("Citations Per Year")
selected_author = st.selectbox("Author Name:", df["name"].unique(), index=0)

author_table = df[df["name"] == selected_author]

with st.expander("Author Info"):
    row = author_table.iloc[0]
    st.json(
        {
            "Name": row["name"],
            "Affiliation": row["affiliation"],
            "hIndex": row["h_index"],
            "i10 Index": row["i10_index"],
            "Publication Count": row["pub_count"],
            "Total Citations": row["cited_by"],
        }
    )


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


def remove_author(name):
    # TODO: adjust to email
    df = pd.read_csv("data/scholars.csv")
    if name not in df.Name.unique():
        st.error("Could not find you.")
        return False
    df = df[df["Name"] != name]
    df.to_csv("data/scholars.csv", index=False)
    return True


st.header("Unsubscribe")
st.markdown(
    """
To unsubscribe from the bot, enter your email and click submit.
"""
)

with st.form("unsubscribe-form"):
    email = st.text_input("Email:")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        if remove_author(email):
            st.success("You are now unsubscribed from the bot.")
