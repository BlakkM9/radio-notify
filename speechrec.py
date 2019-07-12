import requests
import json
import speech_recognition as sr
from pydub import AudioSegment
import smtplib
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import os
import time

import utils

def main():
    global keywords
    global language
    global radio_name
    global email_receiver

    # load data from json
    with open("data.json") as f:
        data = json.load(f)

    CHECK_INTERVAL = data["check_interval"] # in seconds
    STREAM_URL = data["stream_url"]
    language = data["language"]
    email_receiver = data["email_receiver"]

    # load keywords from file
    fo = open("keywords.txt", "r")
    keywords_combined = fo.read().replace("\n", "")
    keywords = keywords_combined.split(",")

    s_print("Keywords(" + str(len(keywords)) + "):")
    for i in keywords:
        s_print(i)
    print()

    # get radio name
    r = requests.get(STREAM_URL, stream=True)
    radio_name = utils.get_radio_name(r.headers)

    # set ffmpeg path
    AudioSegment.converter = os.path.dirname(os.path.abspath(__file__)) + "\\ffmpeg\\bin\\ffmpeg"

    # start loop that checks if new file is ready
    while True:
        f = []
        for (dirpath, dirnames, filenames) in os.walk("./rec"):
            f.extend(filenames)
            break
        if ("ready.mp3" in f):
            recognize()

        time.sleep(CHECK_INTERVAL)

def recognize():
        # convert to wav
        current = AudioSegment.from_mp3("./rec/ready.mp3")
        current.export("./rec/current.wav", format="wav")

        # rename mp3 file
        os.rename("./rec/ready.mp3", "./rec/current.mp3")

        r = sr.Recognizer()
        with sr.AudioFile("./rec/current.wav") as source:
            audio = r.record(source)

        # delete wav file
        os.remove("./rec/current.wav")

        try:
            rec_text = r.recognize_google(audio, language=language)
            s_print("RECOGNIZED TEXT:\n" + rec_text)

            # check if result contains one of the keywords
            found_words = []
            for i in keywords:
                if contains_word(i, rec_text):
                    found_words.append(i)

            # send list of found words per send_email
            if len(found_words) != 0:
                send_email(found_words)
            else:
                s_print("NO KEYWORDS")

        except sr.UnknownValueError:
            s_print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            s_print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # delete current mp3 file
        os.remove("./rec/current.mp3")


def send_email(found_words):

    # combine found words
    found_words_combined = ""

    for i in range(0, len(found_words)):
        found_words_combined += found_words[i]
        if i < (len(found_words) - 1):
            found_words_combined += ", "

    s_print("KEYWORDS FOUND: " + found_words_combined)

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

def contains_word(w, string):
    return re.compile(r"\b({0})\b".format(w), flags=re.IGNORECASE).search(string)

def s_print(string):
    print("[S] " + string)

main()
