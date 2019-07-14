import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import data


def send_email(found_words_combined):

    # build e-mail
    sender = "info@radio-notify.com"

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = data.email_receiver
    message["Subject"] = "Keyword was mentionen on " + data.radio_name

    # body
    body = "Found keywords: " + found_words_combined + "."
    message.attach(MIMEText(body, "plain"))

    # attachment
    with open("./rec/current.mp3", "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
            "Content-Disposition",
            f"attachment; filename=occurence.mp3",
    )

    message.attach(part)

    text = message.as_string()

    # send e-mail
    try:
        server = smtplib.SMTP("localhost")
        server.sendmail(sender, data.email_receiver, text)
        server.close()
        e_print("Successfully send e-mail")
    except smtplib.SMTPException as e:
        e_print("Failed to send e-mail " + str(e))


def e_print(string):
    print("[E] " + string)
