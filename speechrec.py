import speech_recognition as sr
from pydub import AudioSegment
import os
import time

def main():
    # set ffmpeg path
    AudioSegment.converter = os.path.dirname(os.path.abspath(__file__)) + "\\ffmpeg\\bin\\ffmpeg"

    # start loop that checks if new recording file is present
    while True:
        f = []
        for (dirpath, dirnames, filenames) in os.walk("./rec"):
            f.extend(filenames)
            break
        if ("ready.mp3" in f):
            recognize()

        time.sleep(5)

def recognize():
        # convert to wav
        current = AudioSegment.from_mp3("./rec/ready.mp3")
        current.export("./rec/current.wav", format="wav")

        # delete mp3 file
        os.remove("./rec/ready.mp3")

        r = sr.Recognizer()
        with sr.AudioFile("./rec/current.wav") as source:
            audio = r.record(source)

        try:
            s_print("RESULT: " + r.recognize_google(audio, language="de-DE"))
        except sr.UnknownValueError:
            s_print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            s_print("Could not request results from Google Speech Recognition service; {0}".format(e))

        os.remove("./rec/current.wav")

def s_print(string):
    print("[S] " + string)

main()
