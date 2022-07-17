import cv2
from numba import njit
from numba.typed import List
from os import get_terminal_size
import numpy as np
import colorama

colorama.init(convert = True, wrap = True, autoreset=False, strip = None)

def resize_dims(frame):
    height = get_terminal_size().lines-10
    cmd_width = get_terminal_size().columns
    SCALE = frame.shape[1]/frame.shape[0]
    width = int(height*SCALE*2)
    padding = int(cmd_width*0.20)
    
    #-----------------------------------------------#
                    #Scaling#
    #-----------------------------------------------#
    dsize = (width,height)

    return dsize, padding


@njit
def render(frame, padding, ASCII_CHARS):
    
    #-----------------------------------------------#
                    #Image Iteration#
    #-----------------------------------------------#


    for row in frame:

        char_row = [ASCII_CHARS[int(pixel*0.098071)] for pixel in row]
        char_multi_row = " " * padding + "".join(char_row)
        print(LINE_CLEAR)
        print(LINE_UP + char_multi_row)




#-----------------------------------------------#
        #Set Ascii Array By Intensity#
#-----------------------------------------------#

ascii = ["@","&","#","¤","W","M","N","£","$","%","O","X","L","/","=","+","_","!",";",":","*","~","-",",","."," "]
ascii.reverse()
ASCII_CHARS = List(ascii)
#-----------------------------------------------#
            #Initialize Video#
#-----------------------------------------------#

video_path = input(f"> Please specify a video file path: ")
cap = cv2.VideoCapture(video_path)




#-----------------------------------------------#
                #Main While Loop#
#-----------------------------------------------#

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

count = 0

while (True):
    _, frame = cap.read()

    if frame is not None:
        if (count%20) == 0:
            dsize, padding = resize_dims(frame)

        frame1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame1, dsize)
        
        render(frame, padding, ASCII_CHARS)

        cv2.imshow("Video Out",frame)

        if cv2.waitKey(1) & 0xFF == ord('p'):
            if cv2.waitKey(0) & 0xFF == ord('p'):
                continue
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                print((LINE_UP + '\r')*len(frame+1), end='\r')
                break

        print((LINE_UP + '\r')*len(frame+1), end='\r')

        count += 1

    else:
        print((LINE_UP + '\r')*len(frame+1), end='\r')
        print("Video Over.")
        break

cap.release()
cv2.destroyAllWindows()
colorama.deinit()




