import cv2
import colorama
from Stream import FileVideoStream
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
        
        #char_row = [ASCII_CHARS[round((pixel*color_const))] for pixel in row]
        char_multi_row = " " * padding + "".join([ASCII_CHARS[round((pixel*color_const))] for pixel in row])
        print(LINE_CLEAR)
        print(LINE_UP + char_multi_row)
    
    print((LINE_UP + '\r')*len(frame+1), end='\r')



colorama.init(convert = True, wrap = True, autoreset=False, strip = None)
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

Ascii =   ("@","&","#","¤","M","N","£","$","%","O","X","L","|","/","=","!",";",":","*","~","-",",","."," ")
ASCII = Ascii[::-1]
color_const = (len(ASCII)-1)/255

size = 640
video_path = input(f"> Please specify a video file path: ")
fvs = FileVideoStream(video_path, queue_size=size).start()
while(not fvs.Q.full() and not fvs.stopped):
    print(f"LOADING .. {fvs.Q.qsize()} done of {size} ...",end = '\r')
dsize = (None, None)

while fvs.running():
    
    dsize, padding = fvs.calc_size(fvs.SCALE)
    
    fvs.update(dsize, padding)


    while fvs.more():
        frame, padding = fvs.read()

        #render(frame, padding, ASCII)
        for row in frame:
        
            #char_row = [ASCII_CHARS[round((pixel*color_const))] for pixel in row]
            char_multi_row = " " * padding + "".join([ASCII[round((pixel*color_const))] for pixel in row])
            print(LINE_CLEAR)
            print(LINE_UP + char_multi_row)
        
        print((LINE_UP + '\r')*len(frame+1), end='\r')
        #cv2.imshow("Video Out",frame)



if dsize[0] is not None:
    _, height = dsize
    print(LINE_UP*(height+1), end = LINE_CLEAR)
    print("Video Over.")



cv2.destroyAllWindows()
colorama.deinit()