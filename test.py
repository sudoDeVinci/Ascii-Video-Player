from datetime import datetime
from os import get_terminal_size, system
from platform import platform

from cv2 import (CAP_PROP_FRAME_COUNT, COLOR_BGR2GRAY, VideoCapture, cvtColor,
                 resize)

# Check if on windows or unix system
try:
    current_os = platform().system()
except Exception:
    current_os = "N/A"

# If current OS is windows, call system() to allow for ansi codes to work.
# NO clue why this works but found here:
# https://stackoverflow.com/questions/12492810/python-how-can-i-make-the-ansi-escape-codes-to-work-also-in-windows

if current_os.lower().__contains__("windows"):
    system("")


# ANSI chars used for cursor movement for rendering
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'


# The ascii characters used to render our video in terminal
Ascii = ("@", "&", "#", "¤", "M", "N", "£",
         "$", "%", "O", "X", "L", "|", "/",
         "=", "!", ";", ":", "*", "~", "-",
         ",", ".", " ")

# Ascii = '@&#¤MN£$%OXL|/=!;:*~-,. '
ASCII = Ascii[::-1]
color_const = (len(ASCII)-1)/255


# Take media path for video included file extension
video_path = input("> Please specify a video file path: ")


# Attempt reading first frame
stream = VideoCapture(video_path)
grabbed, frame = stream.read()


# If first frame read, scale to the current terminal window size.
if grabbed:
    SCALE = frame.shape[1]/frame.shape[0]
    height = int(get_terminal_size().lines*0.9)
    cmd_width = get_terminal_size().columns
    width = int(height*SCALE*1.5)

    # Padding the left and right sides of the terminal to stop line overflow
    # padding_size = int(cmd_width*0.2)
    padding = " " * int(cmd_width*0.2)

    dsize = (width, height)
    frames = 0

    # Attempt to get the number of frames in our video
    # Unsure for now what to do without total number so we handle it
    try:
        total_frames = int(stream.get(CAP_PROP_FRAME_COUNT))
    except Exception:
        total_frames = None

# Start timer for benchmark
start = datetime.now()


while grabbed:
    frame = resize(frame, dsize)
    frame = cvtColor(frame, COLOR_BGR2GRAY)

    whole_ascii_frame = (''.join((ASCII[int((pixel*color_const))] for pixel in row)) for row in frame)
    for ascii_row in whole_ascii_frame:
        print(f"{LINE_CLEAR} {padding}{ascii_row}")

    print(f"{LINE_UP} \r"*len(frame), end='\r')
    frames += 1

    grabbed, frame = stream.read()

# End benchmark timer
end = datetime.now()
print(f" \n {LINE_CLEAR} Time: {end -  start} Frames: {frames}/{total_frames}")
