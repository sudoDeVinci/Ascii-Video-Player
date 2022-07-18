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
from os import get_terminal_size
import cv2
from time import sleep
# import the Queue class from Python 3
if version_info >= (3, 0):
	from queue import Queue
# otherwise, import the Queue class for Python 2.7
else:
	from Queue import Queue



class FileVideoStream:


    def __init__(self, path, queue_size=128):
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
            # intialize thread
            self.thread = Thread(target=self.update, args=())
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
    
    def update(self):
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
                    

                # add the frame to the queue
                self.Q.put(frame)
            else:
                sleep(0.1)  # Rest for 10ms, we have a full queue

        

    
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

