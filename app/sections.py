import streamlit as st
import pandas as pd


def sidebar_content():
    with st.sidebar:
        st.image(
            "static/img/IPOP-logo.png",
            caption="UK Institute for Pharmaceutical Outcomes and Policy",
            width=None,
            use_column_width=True,
            output_format="auto",
        )

        # unsubscribe section
        st.header("Unsubscribe")
        st.markdown(
            """
        To unsubscribe from the bot, enter your email and click submit.
        """
        )
        with st.form(key="unsubscribe-form"):
            email = st.text_input("Email:")
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted and remove_author(email):
                st.success("You are now unsubscribed from the bot.")


def remove_author(name):
    # TODO: adjust to email
    df = pd.read_csv("data/scholars.csv")
    if name not in df.Name.unique():
        st.error("Could not find you.")
        return False
    df = df[df["Name"] != name]
    df.to_csv("data/scholars.csv", index=False)
    return True
