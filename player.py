from multiprocessing import Queue, Process
from time import perf_counter
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
render_delay = 0



def read_frames(video_path: str, queue: Queue, init: bool = False) -> None:
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
        #print(f"grabbed: init  = {init}")
        SCALE = frame.shape[1]/frame.shape[0]
        height = int(get_terminal_size().lines*0.9)
        cmd_width = get_terminal_size().columns
        width = int(height*SCALE*1.5)

        # Padding the left and right sides of terminal to stop line overflow
        # padding_size = int(cmd_width*0.2)
        padding = " " * int(cmd_width*0.2)

        dsize = (width, height)
        if init:
            fps = stream.get(5)
            full_ascii_frame = [''.join(("@" for _ in range(width))) for _ in range(height)]
            empty_ascii_frame = [''.join((" " for _ in range(width))) for _ in range(height)]
            for _ in range(30):
                queue.put((height, padding, full_ascii_frame))
                queue.put((height, padding, empty_ascii_frame))
            queue.put((None, None, None))
            return fps

    while grabbed:
        frame = resize(frame, dsize)
        frame = cvtColor(frame, COLOR_BGR2GRAY)
        
        whole_ascii_frame = [''.join((ASCII[int((pixel*color_const))] for pixel in row)) for row in frame]
        queue.put((height, padding, whole_ascii_frame))
        grabbed, frame = stream.read()
    
    stream.release()
    
    queue.put((None, None, None))
    return None



def draw_frames(queue: Queue) -> None:
    global render_delay
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
        sleep(render_delay)


def render(video_path: str) -> None:
    global render_delay
    # Video frame queue
    queue = Queue(maxsize=600)

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
        #print("getting delay")
        fps = read_frames(video_path, queue, True)
        target_frame_delay = 1.0/fps
        #print("getting start")
        start = perf_counter()
        #print("drawing frame")
        draw_frames(queue)
        #print("getting render time")
        end = perf_counter()

        avg_render_time = (end-start)/60
        print(f"FPS: {fps}\nAverage render time: {avg_render_time:0.4f} seconds\nTarget render delay: {target_frame_delay:.04f} seconds\n")

        if target_frame_delay > avg_render_time:
           delay_delta = target_frame_delay - avg_render_time
           if delay_delta > 0:
                render_delay = delay_delta


        
    except Exception:
        print("Exception reading video stream - calibration section")
        return None

    # Producer process
    producer = Process(target=read_frames, args=(video_path, queue,))
    producer.start()

    # Consumer process - 1.0 second delay to allow producer a buffer.
    sleep(1.0)
    consumer = Process(target=draw_frames, args=(queue,))
    consumer.start()
    
    # Process join
    producer.join()
    consumer.join()


    

