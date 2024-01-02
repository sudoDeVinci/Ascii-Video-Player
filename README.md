# Ascii-Video-Generator

A script to convert video frames into ascii art and display them in the command line.

- Rather than the usual contuous scrolling, we use ANSI colour codes to manipulate the cursor. We can use this to redraw the current window, as well as resize the frames to the window dynamically.

- A simple threaded queue was added to allow a buffer of frames to exist for smoother playback.

- Framerate targets allow for adjusting the terminal size for better playback depedning on the system abilities. The player is very much IO bound as you'd expect.

- This downsizes a given video and converts it into ascii art frame by frame. This works simply by matching the "pixel density" of a given ascii character to a light intensity range of a pixel within a greyscaled version of the video. An example can be seen below:

![example raster](media/example.gif "example raster")
