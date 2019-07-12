import os
import subprocess

# create rec dir if not existing
if (not(os.path.exists("./rec") and os.path.isdir("./rec"))):
    os.mkdir("./rec")

# start stream saver
a = subprocess.Popen(["python", "audiostream.py"])

# start speech recogizer
s = subprocess.Popen(["python", "speechrec.py"])

try:
    a.wait() or s.wait()
except KeyboardInterrupt:
    a.terminate()
    s.terminate()
