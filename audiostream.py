import requests
import json
import os
import re

import utils

# stream urls for testing
# https://mp3channels.webradio.de/antenne?&aw_0_1st.playerid=AntenneBayernWebPlayer&aw_0_1st.listenerid=undefined&aw_0_1st.skey=1562885282&aw_0_1st.gpslat=47.852&aw_0_1st.gpslong=8.77&aw_0_req.gdpr=true&aw_0_1st.spotcom=%5B%5D
# http://sc-trance.1.fm:8040
# http://stream.laut.fm/hoerspieltalk

def main():
    # load data from json
    with open("data.json") as f:
        data = json.load(f)

    RECORDING_LENGTH = data["recording_length"]
    STREAM_URL = data["stream_url"]

    # get stream
    r = requests.get(STREAM_URL, stream=True)
    # extract bitrate
    bitrate = r.headers["icy-br"]
    try:
        # check if only int number was in header
        int(bitrate)
    except:
        # try to parse
        a_print(bitrate + " is invalid bitrate format, parsing")
        rates = re.split(r"\D+", bitrate)
        bitrate = rates[0]

    # get radio name
    radio_name = utils.get_radio_name(r.headers)

    # a_print(str(r.headers))

    a_print("Stream URL: " + STREAM_URL)
    a_print("Station name: " + radio_name)
    a_print("Bitrate: " + bitrate)

    needed_iterations = round((int(bitrate) * RECORDING_LENGTH) / 8);

    a_print("Iterations: " + str(needed_iterations))

    print()

    while True:
        a_print("Starting new file")
        iterations = 0
        with open("./rec/recording.mp3", "wb") as f:
            for block in r.iter_content(1024):
                f.write(block)
                iterations += 1
                if (iterations == needed_iterations):
                    break

        # rename file so speechrec knows it is ready
        os.rename("./rec/recording.mp3", "./rec/ready.mp3")

def a_print(string):
    print("[A] " + string)

main()
