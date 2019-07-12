import speech_recognition as sr
from pydub import AudioSegment
import os
import time

CHECK_INTERVALL = 5 # in seconds

def main():
    # set ffmpeg path
    AudioSegment.converter = os.path.dirname(os.path.abspath(__file__)) + "\\ffmpeg\\bin\\ffmpeg"

    global keywords

    # load keywords from file
    fo = open("keywords.txt", "r")
    keywords_combined = fo.read()
    keywords = keywords_combined.split(",")

    s_print("Keywords(" + str(len(keywords)) + "):")
    for i in keywords:
        s_print(i)

    # start loop that checks if new file is ready
    while True:
        f = []
        for (dirpath, dirnames, filenames) in os.walk("./rec"):
            f.extend(filenames)
            break
        if ("ready.mp3" in f):
            recognize()

        time.sleep(CHECK_INTERVALL)

def recognize():
        # convert to wav
        current = AudioSegment.from_mp3("./rec/ready.mp3")
        current.export("./rec/current.wav", format="wav")

        # delete mp3 file
        os.remove("./rec/ready.mp3")

        r = sr.Recognizer()
        with sr.AudioFile("./rec/current.wav") as source:
            audio = r.record(source)

        # delete wav file
        os.remove("./rec/current.wav")

        try:
            result = r.recognize_google(audio, language="de-DE")
            s_print("RESULT: " + result)

            # check if result contains one of the keywords
            for i in keywords:
                if " " + i + " " in result:
                    s_print("KEYWORD FOUND: " + i)
        except sr.UnknownValueError:
            s_print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            s_print("Could not request results from Google Speech Recognition service; {0}".format(e))


def s_print(string):
    print("[S] " + string)

main()
