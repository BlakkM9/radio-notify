import requests
import os
import re

import data


def main():
    # get stream
    r = requests.get(data.stream_url, stream=True)
    # extract bitrate
    bitrate = r.headers["icy-br"]
    try:
        # check if only int number was in header
        int(bitrate)
    except ValueError:
        # try to parse
        a_print(bitrate + " is invalid bitrate format, parsing")
        rates = re.split(r"\D+", bitrate)
        bitrate = rates[0]

    a_print("Stream URL: " + data.stream_url)
    a_print("Station name: " + data.radio_name)
    a_print("Bitrate: " + bitrate)

    needed_iterations = round((int(bitrate) * data.recording_length) / 8)

    a_print("Iterations: " + str(needed_iterations))

    print()

    while True:
        a_print("Recording new file")
        iterations = 0
        with open("./rec/recording.mp3", "wb") as f:
            for block in r.iter_content(1024):
                f.write(block)
                iterations += 1
                if iterations == needed_iterations:
                    break

        # rename file so speechrec knows it is ready
        os.rename("./rec/recording.mp3", "./rec/ready.mp3")


def a_print(string):
    print("[A] " + string)


main()
