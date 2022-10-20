from array import array
import string
from cv2 import resize, cvtColor, COLOR_BGR2GRAY, VideoCapture
from os import get_terminal_size
from time import sleep
"""
Take in a frame from a queue then process it
"""

from queue import Empty, Queue


# Takes frames from the video capture, processes and puts them in the frame queue
def fill_frame_queue(queue: Queue, cap: VideoCapture, ASCII, color_const: float, padding: int, dsize):

    grabbed, frame = cap.read()

    while grabbed: 
        frame = resize(frame, dsize)
        frame = cvtColor(frame, COLOR_BGR2GRAY)
        char_multi_row_list = []


        for row in frame:
            char_multi_row_list.append(" " * padding + "".join((ASCII[round((pixel*color_const))] for pixel in row)))


        # Put the frame string into the queue
        queue.put(char_multi_row_list)
        
        grabbed, frame = cap.read()
    
    # Put 'None' at the end to indicate end of file.
    queue.put(None)



def render_from_queue(queue: Queue, LINE_UP: str, LINE_CLEAR: str):

    while True:
        #Get a frame from the queue
        try:
            frame = queue.get()
            if frame is None:
                break
            
            for row in frame:
                print(LINE_CLEAR)
                print(LINE_UP + row)
        
            print((LINE_UP + '\r')*(len(frame)+1), end='\r')

        except Empty:
            continue

