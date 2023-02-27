from multiprocessing import Queue, Process
from datetime import datetime
from os import get_terminal_size, system
from platform import platform

from cv2 import COLOR_BGR2GRAY, VideoCapture, cvtColor, resize



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



def read_frames(video_path: str, queue: Queue):
    try:
        # Attempt reading first frame
        stream = VideoCapture(video_path)
        #stream = VideoCapture(0)
        grabbed, frame = stream.read()
    except Exception:
        print("Exception reading video stream")
        queue.put((None, None, None))
        return None


    # If first frame read, scale to the current terminal window size.
    if grabbed:
        SCALE = frame.shape[1]/frame.shape[0]
        height = int(get_terminal_size().lines*0.9)
        cmd_width = get_terminal_size().columns
        width = int(height*SCALE*1.5)

        # Padding the left and right sides of terminal to stop line overflow
        # padding_size = int(cmd_width*0.2)
        padding = " " * int(cmd_width*0.2)

        dsize = (width, height)

    while grabbed:
        frame = resize(frame, dsize)
        frame = cvtColor(frame, COLOR_BGR2GRAY)
        
        whole_ascii_frame = [''.join((ASCII[int((pixel*color_const))] for pixel in row)) for row in frame]
        queue.put((len(frame), padding, whole_ascii_frame))

        grabbed, frame = stream.read()
    
    stream.release()
    
    queue.put((None, None, None))

def draw_frames(queue: Queue):
    while True:
        # get frame from queue
        frame_length, padding, whole_ascii_frame = queue.get()

        if frame_length is None:
            break

        for ascii_row in whole_ascii_frame:
            print(f"{LINE_CLEAR} {padding}{ascii_row}", flush=True)
        print(f"{LINE_UP} \r"*frame_length, end='\r', flush=True)


if __name__ == "__main__":
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
        from colorama import just_fix_windows_console_colors
        just_fix_windows_console_colors()


    # Take media path for video included file extension
    video_path = input("> Please specify a video file path: ")

    # Video frame queue
    queue = Queue(maxsize=1000)

    # Producer process
    producer = Process(target=read_frames, args=(video_path, queue,))
    producer.start()

    # Consumer process
    consumer = Process(target=draw_frames, args=(queue,))
    consumer.start()
    

    producer.join()
    consumer.join()
    

