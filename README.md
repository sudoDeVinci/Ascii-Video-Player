# Ascii-Video-Generator

A script to convert video frames into ascii art and display them in the command line.

This downsizes a given video and converts it into ascii art frame by frame.
This works simply by matching the "pixel density" of a given ascii character to a light intensity range of a pixel within a greyscaled version of the video.
This has no real uses but it was fun to build either way.
An example can be seen below:

![example raster](media/example.gif "example raster")


A simple threaded queue was added to allow a buffer of frames to exist for smoother playback
