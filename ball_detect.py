# import the necessary packages

import numpy as np
import cv2 as cv

 
 
# Define fution to resize the vido frame size
def rescaleFunc(frame,scale = 0.5):
    width  = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimension = (width,height)
    rescalar = cv.resize(frame,dimension,interpolation = cv.INTER_AREA)

    return rescalar

# Video Path
cap = cv.VideoCapture("C:\\Users\\gangw\\OneDrive\\Desktop\\AI Assignment video.mp4")
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)+(y1-y2)
# define the lower and upper boundaries of the colors in the HSV color space
sensitivity = 15
lower = {'red':(166, 84, 141), 'green':(40, 52, 72),  'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'white':(208,208,208), 'orange':(2, 50, 80)} 
upper = {'red':(186,255,255),  'green':(102,255,255), 'blue':(117,255,255),  'yellow':(54,255,255),  'white':(255,255,255), 'orange':(10,255,255)}

# define standard colors for circle around the object
colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217),'white':(0,0,0), 'orange':(0,140,255)}
 
while True:
    timer = cv.getTickCount()
    success, img = cap.read()
    frame_resize = rescaleFunc(img)

    grayFrame = cv.cvtColor(frame_resize,cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame,(17,17),0)

    circles = cv.HoughCircles(blurFrame,cv.HOUGH_GRADIENT,1.2,100,
        param1 = 100,param2 = 30,minRadius = 0 ,maxRadius = 40)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None

        for i in circles[0,:]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1])==dist(i[0],i[1],prevCircle[0],prevCircle[1]):
                    chosen = i

        cv.circle(frame_resize,(chosen[0],chosen[1]),1,(0,100,100),3)
        cv.circle(frame_resize,(chosen[0],chosen[1]),chosen[2],(255,0,255),3)
        prevCircle = chosen

    cv.imshow("circles",frame_resize)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

