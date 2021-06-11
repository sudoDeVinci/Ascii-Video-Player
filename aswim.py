import cv2


ASCII_CHARS=["@","#","&","¤","W","M","N","£","$","%","O","X","L","(","/","_","+","!",";",":","*","-",",","."," "]
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
cv2.createTrackbar("Height","Playback",54,100,nothing)
cv2.createTrackbar("Width","Playback",208,300,nothing)
cv2.createTrackbar("FrameTime","Playback",12,50,nothing)


#-----------------------------------------------#
                    #Main While Loop#
#-----------------------------------------------#


while playing:

    height = cv2.getTrackbarPos("Height","Playback")
    width = cv2.getTrackbarPos("Width","Playback")
    frametime = cv2.getTrackbarPos("FrameTime","Playback")
    if frametime == 0:
        frametime = 1

    playing,frame = cap.read()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #-----------------------------------------------#
                        #Scaling#
    #-----------------------------------------------#


    dsize = (width,height)

    frame = cv2.resize(frame, dsize)
    
    
    #-----------------------------------------------#
                        #Image Iteration#
    #-----------------------------------------------#
    
    char_multi_row = "\n"
    for row in frame:
        
        char_row=[]

        for pixel in row:
            char_value = int(pixel/11)
            char_row.append(ASCII_CHARS[char_value])
        
        char_multi_row += "".join(char_row)
        char_multi_row += "\n"

    print(char_multi_row)

    cv2.imshow("Video Out",frame)
    if cv2.waitKey(frametime) & 0xFF == ord('q'):
        break

