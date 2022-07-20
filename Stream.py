"""
The MIT License (MIT)

Copyright (c) 2015-2016 Adrian Rosebrock, http://www.pyimagesearch.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from threading import Thread
from sys import version_info
import cv2
from time import sleep
from os import get_terminal_size
# import the Queue class from Python 3
if version_info >= (3, 0):
	from queue import Queue
# otherwise, import the Queue class for Python 2.7
else:
	from Queue import Queue



class FileVideoStream:


    def __init__(self, path, queue_size=64):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(path)
        try:
            _, frame = self.stream.read()
            self.SCALE = frame.shape[1]/frame.shape[0]
            self.stopped = False
            # initialize the queue used to store frames read from
            # the video file
            self.Q = Queue(maxsize=queue_size)

            # Get dsize
            dsize, padding = self.calc_size(self.SCALE)
            # intialize thread
            self.thread = Thread(target=self.update, args=(dsize, padding))
            self.thread.daemon = True
            self.frames = 0
        except Exception as e:
            print(e)
            self.stopped = True

    def start(self):
        # start a thread to read frames from the file video stream
        self.thread.start()
        self.stopped = False
        return self
    
    def update(self, dsize, padding):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                break

            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()

                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stopped = True
                    self.stream.release()
                    break
                    

                # add the frame to the queue

                ## First I want to increase contrast
                frame = self.up_contrast(frame) 


                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                frame = cv2.resize(frame, dsize)
                self.Q.put((frame, padding))
            else:
                sleep(0.05)  # Rest for 10ms, we have a full queue

        

    
    def read(self):
        # return next frame in the queue
        return self.Q.get()

    def running(self):
        return self.more() or not self.stopped

    def more(self):
        # return True if there are still frames in the queue. If stream is not stopped, try to wait a moment
        tries = 0
        while self.Q.qsize() == 0 and not self.stopped and tries < 5:
            sleep(0.1)
            tries += 1

        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        # wait until stream resources are released (producer thread might be still grabbing frame)
        self.thread.join()


    def calc_size(self, SCALE):
        height = get_terminal_size().lines-10
        cmd_width = get_terminal_size().columns
        width = int(height*SCALE*2)
        padding = int(cmd_width*0.20)
        
        #-----------------------------------------------#
                        #Scaling#
        #-----------------------------------------------#
        dsize = (width,height)

        return dsize, padding
    
    def up_contrast(self, frame):
        """
        Code from: Jeru Luke, Answer #1 at
        https://discuss.dizzycoding.com/how-do-i-increase-the-contrast-of-an-image-in-python-opencv/
        """
        #-----Converting image to LAB Color model----------------------------------- 
        lab= cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

        #-----Splitting the LAB image to different channels-------------------------
        l, a, b = cv2.split(lab)

        #-----Applying CLAHE to L-channel-------------------------------------------
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)

        #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
        limg = cv2.merge((cl,a,b))

        #-----Converting image from LAB Color model to RGB model--------------------
        final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

        return final
