import requests

RECORDING_LENGTH = 120 # in seconds (= 2 min)

# stream_url = "https://mp3channels.webradio.de/antenne?&aw_0_1st.playerid=AntenneBayernWebPlayer&aw_0_1st.listenerid=undefined&aw_0_1st.skey=1562885282&aw_0_1st.gpslat=47.852&aw_0_1st.gpslong=8.77&aw_0_req.gdpr=true&aw_0_1st.spotcom=%5B%5D"
stream_url = "http://sc-trance.1.fm:8040"

r = requests.get(stream_url, stream=True)
# get bitrate
bitrate = r.headers["icy-br"]

neededIterations = round((int(bitrate) * RECORDING_LENGTH) / 8);

print("Bitrate: " + bitrate)
print("Iterations: " + str(neededIterations))
part = 0
while part < 5:
    iterations = 0
    with open("./rec/stream" + str(part) + ".mp3", "wb") as f:
        for block in r.iter_content(1024):
            f.write(block)
            iterations += 1
            if (iterations == neededIterations):
                break;
        part += 1
