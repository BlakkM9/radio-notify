def get_radio_name(headers):
    if "X-RadioName" in headers:
        radio_name = headers["X-RadioName"]
    elif "icy-name":
        radio_name = headers["icy-name"]
    else:
        radio_name = "Unknown Name"
    return radio_name
