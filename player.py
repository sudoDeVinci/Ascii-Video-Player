from multiprocessing import Queue, Process
from datetime import datetime
from os import get_terminal_size, system
from platform import platform
from time import sleep
from cv2 import COLOR_BGR2GRAY, VideoCapture, cvtColor, resize, CAP_PROP_FPS



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



def read_frames(video_path: str, queue: Queue) -> None:
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
    
        fps = stream.get(5) #int fps
        # width  = stream.get(3)  # float `width`
        # height = stream.get(4)  # float `height`
        frame_delay = 1/fps
        dummy_frame = dummy_frame_full()
        queue.put()

    while grabbed:
        frame = resize(frame, dsize)
        frame = cvtColor(frame, COLOR_BGR2GRAY)
        
        whole_ascii_frame = [''.join((ASCII[int((pixel*color_const))] for pixel in row)) for row in frame]
        queue.put((len(frame), padding, whole_ascii_frame))

        grabbed, frame = stream.read()
    
    stream.release()
    
    queue.put((None, None, None))



def draw_frames(queue: Queue) -> None:
    sleep(1.0)
    while True:
        # get frame from queue
        frame_length, padding, whole_ascii_frame = queue.get()

        if frame_length is None:
            break
        
        line = ""
        for ascii_row in whole_ascii_frame:
            #print(f"{LINE_CLEAR} {padding}{ascii_row}", flush=True)
            line += f"{LINE_CLEAR} {padding}{ascii_row}\n"
        print(line[:-1])
        print(f"{LINE_UP} \r"*frame_length, end='\r', flush=True)


def dummy_frame_full(height, width) -> str:
    symbol = ASCII[0]
    frame = (f"{LINE_CLEAR} {symbol*width}\n" for _ in height)
    return '/n'.join(frame)



def render(video_path: str) -> None:
    # Video frame queue
    queue = Queue(maxsize=10000)

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

    
    #Initialize the player by checking rendering time for a single frame
    try:
        # Attempt reading framerate
        stream = VideoCapture(video_path)
        #stream = VideoCapture(0)
        fps = stream.get(5) #int fps
        width  = stream.get(3)  # float `width`
        height = stream.get(4)  # float `height`
        frame_delay = 1/fps

        SCALE = frame.shape[1]/frame.shape[0]
        height = int(get_terminal_size().lines*0.9)
        cmd_width = get_terminal_size().columns
        width = int(height*SCALE*1.5)

        # Padding the left and right sides of terminal to stop line overflow
        # padding_size = int(cmd_width*0.2)
        padding = " " * int(cmd_width*0.2)

        dsize = (width, height)

        dummy_frame = dummy_frame_full()

        
    except Exception:
        print("Exception reading video stream")
        return None

    # Producer process
    producer = Process(target=read_frames, args=(video_path, queue,))
    producer.start()

    # Consumer process
    consumer = Process(target=draw_frames, args=(queue,))
    consumer.start()
    
    # Process join
    producer.join()
    consumer.join()




if __name__ == "__main__":
    render()

    
    

