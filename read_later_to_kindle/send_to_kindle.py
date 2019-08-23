import datetime
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import os
import smtplib

DATE = datetime.datetime.now().strftime("%a, %d %b %Y")
TITLE = "Read Later Digest - {}".format(DATE)
FROM = os.environ["EMAIL_FROM"]
TO = os.environ["EMAIL_TO"]
PASSWORD = os.environ["EMAIL_PASSWORD"]
HOST = os.environ["EMAIL_HOST"]


def send_to_kindle(path, log_path):
    message = _create_message(path, log_path)
    with smtplib.SMTP(host=HOST, port=587) as s:
        s.starttls()
        s.login(FROM, PASSWORD)
        s.send_message(message)


def _create_attachment(path):
    with open(path, "rb") as fp:
        attachment = MIMEBase("text", "html")
        attachment.set_payload(fp.read())
    encoders.encode_base64(attachment)
    filename = "{}.html".format(TITLE)
    attachment.add_header(
        "Content-Disposition", "attachment", filename=filename
    )
    return attachment


def _create_message(path, log_path):
    with open(log_path) as f:
        content = "{}\n\n{}".format(TITLE, f.read())

    message = EmailMessage()
    message["Subject"] = "convert"
    message["From"] = FROM
    message["To"] = TO
    message.preamble = TITLE
    message.set_content(content)
    message.make_mixed()

    attachment = _create_attachment(path)
    message.attach(attachment)

    return message
