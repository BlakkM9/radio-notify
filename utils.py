import os
import subprocess


def combine_string(string_arr, seperator):
    combined = ""

    for i in range(0, len(string_arr)):
        combined += string_arr[i]
        if i < (len(string_arr) - 1):
            combined += seperator

    return combined


curr_path = os.path.abspath(".")


def ffmpeg(input_file, output_file):
    # extract file formats
    input_ext = os.path.splitext(input_file)[1][1:]
    output_ext = os.path.splitext(output_file)[1][1:]

    # convert to absolute paths if necessary
    if os.path.isabs(input_file):
        input_path = input_file
    else:
        input_path = curr_path + input_file

    if os.path.isabs(output_file):
        output_path = output_file
    else:
        output_path = curr_path + output_file

    if output_ext == "wav":
        command = (curr_path + "/ffmpeg/bin/ffmpeg.exe -i " +
                   input_path + " " +
                   output_path)
    elif output_ext == "ogg":
        command = (curr_path + "/ffmpeg/bin/ffmpeg.exe -i " +
                   input_path + " " +
                   "-c:a libopus " +
                   output_path)
    else:
        print("[U] conversion to wav and ogg only!")
        return

    subprocess.check_call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # subprocess.check_call(command)

    print("[U] Converted file from " + input_ext + " to " + output_ext)
