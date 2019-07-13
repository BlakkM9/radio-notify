def get_radio_name(headers):
    if "X-RadioName" in headers:
        radio_name = headers["X-RadioName"]
    elif "icy-name":
        radio_name = headers["icy-name"]
    else:
        radio_name = "Unknown Name"
    return radio_name

def combine_string(string_arr, seperator):
        combined = "";

        for i in range(0, len(string_arr)):
            combined += string_arr[i]
            if i < (len(string_arr) - 1):
                combined += seperator

        return combined
