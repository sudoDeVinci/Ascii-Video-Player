import cv2
from datetime import datetime
import os


#-----------------------------------------------#
                #Set Ascii Array By Intensity#
#-----------------------------------------------#


ASCII_CHARS=["@","&","#","¤","W","M","N","£","$","%","O","X","L","/","=","+","_","!",";",":","*","~","-",",","."," "]
ASCII_CHARS.reverse()


#-----------------------------------------------#
                #Initialize Video#
#-----------------------------------------------#


video_path = input(f"> Please specify a video file path: ")
cap = cv2.VideoCapture(video_path)

playing,frame = cap.read()

frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


#-----------------------------------------------#
                #TrackBar#
#-----------------------------------------------#


def nothing():pass

cv2.namedWindow("Playback")
cv2.createTrackbar("Height","Playback",56,100,nothing)
cv2.createTrackbar("Width","Playback",202,300,nothing)
cv2.createTrackbar("FrameTimeNoProcessing","Playback",13,50,nothing)
#cv2.createTrackbar("FrameTimeProcessing","Playback",0,10000,nothing)


#-----------------------------------------------#
                #Main While Loop#
#-----------------------------------------------#


while playing:

    height = cv2.getTrackbarPos("Height","Playback")
    width = cv2.getTrackbarPos("Width","Playback")
    frametime = cv2.getTrackbarPos("FrameTimeNoProcessing","Playback")
    if frametime == 0:
        frametime = 1

    playing,frame = cap.read()

    #start = float(datetime.now().strftime('%f'))
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


    #-----------------------------------------------#
                    #Scaling#
    #-----------------------------------------------#


    dsize = (width,height)

    frame = cv2.resize(frame, dsize)
    
    
    #-----------------------------------------------#
                    #Image Iteration#
    #-----------------------------------------------#
    

    
    char_multi_row = ""
    for row in frame:
        
        char_row=[]

        for pixel in row:
            char_value = int(pixel/10.8)
            char_row.append(ASCII_CHARS[char_value])
        
        char_multi_row += "".join(char_row)
        char_multi_row += "\n"

    #delta = float(datetime.now().strftime('%f')) - start
    #delta = int(delta)
    #cv2.setTrackbarPos("FrameTimeProcessing","Playback",delta)

    
    print(f"{char_multi_row}")

    cv2.imshow("Video Out",frame)
    if cv2.waitKey(frametime) & 0xFF == ord('q'):
        break






