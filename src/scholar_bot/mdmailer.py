import mdmail


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

mdmail.send(
    email,
    subject="Sample Email",
    from_email="nanthony007@gmail.com",
    to_email="nanthony007@gmail.com",
    smtp=smtp,
)
