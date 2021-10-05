import mdmail
import utils

with open("my-email.md") as f:
    email = f.read()

# Specify SMTP server
smtp = {
    "host": "smtp.gmail.com",
    "port": 587,
    "tls": True,
    "ssl": False,
    "user": "nanthony007@gmail.com",
    "password": "yxoswzfpbihxrjoa",
}

data = utils.get_metrics_change("Chris Delcher")
df = utils.load_data()
row = df[df.name == "Chris Delcher"].iloc[0]


email = f"""
# Hello {data['name']}

Today you are being emailed to update you on the power of Python and automation.

This email contains your updated Google Scholar metrics and how they have changed over the past week.

Hope you enjoy it! :) 

To see your full GS Profile, click [here]({'https://scholar.google.com/citations?user=' + row.gs_id})

| Metric | Change |
| --- | --- |
| h_index | {data['h_index']} |
| i10_index | {data['i10_index']} |
| Citations | {data['cited_by']} |
| Publications | {data['pub_count']} |


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
