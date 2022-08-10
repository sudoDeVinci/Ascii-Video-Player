# Ascii-Video-Generator

A script to convert video frames into ascii art and display them in the command line.

This downsizes a given video and converts it into ascii art frame by frame.
I have also made it so that the framerate, height and width of the video output can be toggled in real time via trackbars.

This works simply by matching the "pixel density" of a given ascii character to a light intensity range of a pixel within a greyscaled version of the video.

This has no real uses but it was fun to build either way.

## Update (18/07/2022)

I removed the ability to resize via trackbars, opting to replace it with the ability of the video to automatically resize itself to the current window dimensions.
To allow for faster playback and higher image resolution in the terminal, The FileVideoStream Class of the [imutils lib](https://github.com/PyImageSearch/imutils/blob/master/imutils/video/filevideostream.py) was used to allow a Queue-Dequeue system for frames.

Rather than simply dumping the output of the current frame into the terminal, the cursor is made to draw each line of a frame, then return to the top left of the screen in preparation for the next frame, similar to scan line technology. Each line is cleared before being printed to.

An example can be seen below:

![example raster](media/example.gif "example raster")
