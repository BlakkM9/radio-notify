import json
import requests


def get_radio_name(headers):
    if "X-RadioName" in headers:
        name = headers["X-RadioName"]
    elif "icy-name" in headers:
        name = headers["icy-name"]
    else:
        name = "Unknown Name"
    return name


# load data from json
with open("data.json") as f:
    data = json.load(f)

recording_length = data["recording_length"]
check_interval = data["check_interval"]
stream_url = data["stream_urls"]["Hoerspieltalk"]
language = data["language"]
email_receiver = data["email_receiver"]
chat_id = data["telegram_chat_id"]

# extract radio name
r = requests.get(stream_url, stream=True)
radio_name = get_radio_name(r.headers)
