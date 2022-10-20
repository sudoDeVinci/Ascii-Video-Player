from queue import Queue
from threading import Thread
from os import get_terminal_size, system
import colorama
from datetime import datetime
from cv2 import resize, cvtColor, COLOR_BGR2GRAY, VideoCapture
from vid_processor import fill_frame_queue, render_from_queue
from platform import platform

# Check if on windows or unix system
try:
    current_os = platform().system()
except:
    current_os = "N/A"

# If current OS is windows, then we use colorama.
if current_os.lower().__contains__("Windows"):
    system("")



# ANSI chars used for cursor movement for rendering
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'


# The ascii characters used to render our video in terminal
Ascii =   ("@","&","#","¤","M","N","£","$","%","O","X","L","|","/","=","!",";",":","*","~","-",",","."," ")
ASCII = Ascii[::-1]
color_const = (len(ASCII)-1)/255
#frames = 0


# Take media path for video included file extension
video_path = input(f"> Please specify a video file path: ")


# Attempt reading first frame
stream = VideoCapture(video_path)
grabbed, frame = stream.read()

if grabbed:
    SCALE = frame.shape[1]/frame.shape[0]
    height = int(get_terminal_size().lines*0.9)
    cmd_width = get_terminal_size().columns
    width = int(height*SCALE*1.5)

    # Padding the left and right sides of the terminal to stop line overflow
    padding = int(cmd_width*0.2)

    dsize = (width,height)


start = datetime.now()

# Create the frame queue
queue = Queue()
size = 32

while grabbed and queue.qsize() <= size:
    print(f"LOADING .. {queue.qsize()} done of {size} ...",end = '\r')
    frame = resize(frame, dsize)
    frame = cvtColor(frame, COLOR_BGR2GRAY)
    char_multi_row_list = []


    for row in frame:
        char_multi_row_list.append(" " * padding + "".join([ASCII[round((pixel*color_const))] for pixel in row]))


    # Put the frame string into the queue
    queue.put(char_multi_row_list)
    
    grabbed, frame = stream.read()
    


# Start filling of the frame queue
buffer = Thread(target = fill_frame_queue, args = (queue, stream, ASCII, color_const, padding, dsize))
buffer.start()

# Start rendering the frames from the buffer
renderer = Thread(target = render_from_queue, args = (queue, LINE_UP, LINE_CLEAR))
renderer.start()

# Join threads
buffer.join()
renderer.join()

end = datetime.now()
#print(frames)
print(end -  start)