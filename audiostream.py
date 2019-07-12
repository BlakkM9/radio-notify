import requests
import os

# constants
RECORDING_LENGTH = 30 # in seconds

# stream_url = "https://mp3channels.webradio.de/antenne?&aw_0_1st.playerid=AntenneBayernWebPlayer&aw_0_1st.listenerid=undefined&aw_0_1st.skey=1562885282&aw_0_1st.gpslat=47.852&aw_0_1st.gpslong=8.77&aw_0_req.gdpr=true&aw_0_1st.spotcom=%5B%5D"
# stream_url = "http://sc-trance.1.fm:8040"
stream_url = "http://stream.laut.fm/hoerspieltalk"

def main():
    r = requests.get(stream_url, stream=True)
    # get bitrate
    bitrate = r.headers["icy-br"]

    needed_iterations = round((int(bitrate) * RECORDING_LENGTH) / 8);

    a_print("Bitrate: " + bitrate)
    a_print("Iterations: " + str(needed_iterations))

    while True:
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
