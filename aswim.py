import cv2
import colorama
from Stream import FileVideoStream
from time import sleep
from os import get_terminal_size



def resize_dims(SCALE):
    height = get_terminal_size().lines-10
    cmd_width = get_terminal_size().columns
    width = int(height*SCALE*2)
    padding = int(cmd_width*0.20)
    
    #-----------------------------------------------#
                    #Scaling#
    #-----------------------------------------------#
    dsize = (width,height)

    return dsize, padding


def render(frame, padding, ASCII_CHARS):

    for row in frame:

        char_row = [ASCII_CHARS[int(pixel*0.098071)] for pixel in row]
        char_multi_row = " " * padding + "".join(char_row)
        print(LINE_CLEAR)
        print(LINE_UP + char_multi_row)



colorama.init(convert = True, wrap = True, autoreset=False, strip = None)
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'


ASCII = ["@","&","#","¤","W","M","N","£","$","%","O","X","L","/","=","+","_","!",";",":","*","~","-",",","."," "]
ASCII.reverse()


video_path = input(f"> Please specify a video file path: ")
fvs = FileVideoStream(video_path).start()
sleep(1.5)
dsize = (None, None)

while fvs.running():
    
    dsize, padding = resize_dims(fvs.SCALE)

    while fvs.more():
        dsize, padding = resize_dims(fvs.SCALE)

        frame = fvs.read()
        if frame is None:
            break
        frame1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame1, dsize)

        render(frame, padding, ASCII)
        cv2.imshow("Video Out",frame)
        print((LINE_UP + '\r')*len(frame+1), end='\r')
    
    fvs.update()



if dsize[0] is not None:
    _, height = dsize
    print(LINE_UP*(height+1), end = LINE_CLEAR)
    print("Video Over.")



cv2.destroyAllWindows()
colorama.deinit()