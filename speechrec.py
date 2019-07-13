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

import tgbot
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
    stream_url = data["stream_url"]
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
    r = requests.get(stream_url, stream=True)
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

            # send string with found words
            if len(found_words) != 0:
                # combine found words
                found_words_combined = utils.combine_string(found_words, ", ")
                s_print("KEYWORDS FOUND: " + found_words_combined)

                # mailbot.send_message(found_words_combined)
                tgbot.send_message(found_words_combined)
            else:
                s_print("NO KEYWORDS")

        except sr.UnknownValueError:
            s_print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            s_print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # delete current mp3 file
        os.remove("./rec/current.mp3")

def contains_word(w, string):
    return re.compile(r"\b({0})\b".format(w), flags=re.IGNORECASE).search(string)

def s_print(string):
    print("[S] " + string)

main()
