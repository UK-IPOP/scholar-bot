# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown

me = "nanthony007@gmail.com"
you = "nanthony007@gmail.com"

textfile = "README.md"

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
with open("README.md", "r") as fp:
    # Create a text/plain message
    message = fp.read()

multipart_msg = MIMEMultipart("alternative")

multipart_msg["Subject"] = "testing automation"
multipart_msg["From"] = me
multipart_msg["To"] = you

html = markdown.markdown(message)
text = message

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
multipart_msg.attach(part2)

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP("smtp.gmail.com", 587)
s.starttls()
s.login("nanthony007@gmail.com", "yxoswzfpbihxrjoa")
s.sendmail(me, [you], multipart_msg.as_string())
s.quit()
