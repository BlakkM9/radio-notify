

def send_email(found_words_combined):

    # build e-mail
    sender = "info@radio-notify.com"

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = email_receiver
    message["Subject"] = "Keyword was mentionen on " + radio_name

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
        server.sendmail(sender, email_receiver, text)
        server.close()
        s_print("Successfully send e-mail")
    except smtplib.SMTPException as e:
        s_print("Failed to send e-mail " + e)
