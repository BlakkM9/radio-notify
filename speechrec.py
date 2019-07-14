import speech_recognition as sr
import re
import os
import time
import textwrap

import tgbot
import utils
import data


def main():
    global keywords

    # load keywords from file
    fo = open("keywords.txt", "r")
    keywords_combined = fo.read().replace("\n", "")
    keywords = keywords_combined.split(",")

    s_print("Keywords(" + str(len(keywords)) + "):")
    for i in keywords:
        s_print(i)
    print()

    # start loop that checks if new file is ready
    while True:

        for item in os.listdir("./rec"):
            if item == "ready.mp3":
                recognize()

        time.sleep(data.check_interval)


def recognize():
    # convert to wav (for speech recogition)
    utils.ffmpeg("./rec/ready.mp3", "./rec/current.wav")

    # convert to ogg (for telegram bot)
    utils.ffmpeg("./rec/ready.mp3", "./rec/current.ogg")

    # rename mp3 (for email bot)
    os.rename("./rec/ready.mp3", "./rec/current.mp3")

    r = sr.Recognizer()
    with sr.AudioFile("./rec/current.wav") as source:
        audio = r.record(source)

    # delete wav file
    os.remove("./rec/current.wav")

    try:
        rec_text = r.recognize_google(audio, language=data.language)

        s_print("RECOGNIZED TEXT:\n" + textwrap.fill(rec_text, 80))

        # check if result contains one of the keywords
        found_words = []
        for i in keywords:
            if contains_word(i, rec_text):
                found_words.append(i)

        # send string with found words
        if len(found_words) != 0:

            # mailbot.send_message(found_words_combined)
            tgbot.send_message(found_words, rec_text)
        else:
            s_print("NO KEYWORDS")

    except sr.UnknownValueError:
        s_print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        s_print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # delete current audio files
    os.remove("./rec/current.ogg")
    os.remove("./rec/current.mp3")


def contains_word(w, string):
    return re.compile(r"\b({0})\b".format(w), flags=re.IGNORECASE).search(string)


def s_print(string):
    print("[S] " + string)


main()
