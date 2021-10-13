import mdmail
import utils


# TODO: this needs to be looped for each author

# Specify SMTP server
smtp = {
    "host": "smtp.gmail.com",
    "port": 587,
    "tls": True,
    "ssl": False,
    "user": "nanthony007@gmail.com",
    "password": "yxoswzfpbihxrjoa",
}

df = utils.load_data()
row = df[df.name == "Chris Delcher"].iloc[0]

change_data = utils.get_metrics_change(row["name"])
email = f"""
# Hello {row['name']}

Today you are being emailed to update you on the power of Python and automation.

This email contains your updated Google Scholar metrics and how they have changed
over the past week.

Hope you enjoy it! :) 

To see your full GS Profile, click
[here]({'https://scholar.google.com/citations?user=' + row['gs_id']})

| Metric       |                Change                 |       Total        |
| :----------- | :----------------------------------:  | :----------------: |
| h_index      |  {round(change_data['h_index'], 2)}%  |  {row["h_index"]}  |
| i10_index    | {round(change_data['i10_index'], 2)}% | {row["i10_index"]} |
| Citations    | {round(change_data['cited_by'], 2)}%  | {row["cited_by"]}  |
| Publications | {round(change_data['pub_count'], 2)}% | {row["pub_count"]} |


Please do not respond to this email as it is automated and unsupervised.

Thank you.

"""

mdmail.send(
    email,
    subject="Sample Email",
    from_email="nanthony007@gmail.com",
    to_email="nanthony007@gmail.com",
    smtp=smtp,
)
