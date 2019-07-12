import os
import subprocess

# create rec dir if not existing
if (not os.path.isdir("./rec")):
    os.mkdir("./rec")

# remove all files in record (if present)
if (os.path.isfile("./rec/current.wav")):
    os.remove("./rec/current.wav")

if (os.path.isfile("./rec/ready.mp3")):
    os.remove("./rec/ready.mp3")

if (os.path.isfile("./rec/recording.mp3")):
    os.remove("./rec/recording.mp3")

if (os.path.isfile("./rec/current.mp3")):
    os.remove("./rec/current.mp3")

# start stream saver
a = subprocess.Popen(["python", "audiostream.py"])

# start speech recogizer
s = subprocess.Popen(["python", "speechrec.py"])

try:
    a.wait() or s.wait()
except KeyboardInterrupt:
    a.terminate()
    s.terminate()
