import cv2
import numpy as np
import sys
from globs import *

cap = cv2.VideoCapture(0)

width = cap.get(3)
height = cap.get(4)

def ce(event, x, y, flags, events):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("coords   x: ", x, " y: ", y)




while 1:
    ret, frame = cap.read()
    if ret is False: 
        continue

    roi = frame

    #roi = cv2.flip(frame, 1)
    roi = frame[190: 265, 250: 425] # frame[140: 290, 170: 250]

    width = 425-250
    height = 265-190

    rows, cols, _ = roi.shape
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)

    _, threshold = cv2.threshold(gray_roi, 20, 255, cv2.THRESH_BINARY_INV)

    contours  = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)

        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 255, 0), 2)
#        cv2.line(roi, (x+int(w/2), 0), (x+int(w/2), rows), (0, 255, 0), 2)
#        cv2.line(roi, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2 )

        cx = x + (((x+w)-x)/2)
        cy = y + (((y+h)-y)/2)


        boundary_left = width/3
        boundary_right = boundary_left * 2
        boundary_up = height/4

        

        ret = E_NONE

        if w > 3*h:
            ret = E_BLINK
        else:
            if cx < boundary_left:
                ret = E_LEFT
            if cx > boundary_right:
                ret = E_RIGHT
            if cy < boundary_up:
                ret = E_UP

        print("\r", ret)
        sys.stdout.flush()
        break

    #cv2.imshow("Threshold", threshold)
    #cv2.imshow("gray roi", gray_roi)

    cv2.namedWindow('Roi', cv2.WND_PROP_FULLSCREEN) #no buttons
    cv2.setWindowProperty('Roi', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    width, height, depth = roi.shape
    scaleW = float(1440)/float(width)
    scaleH = float(900)/float(height)
    nx, ny = width*scaleW, height*scaleH
    print(str(scaleW) + " " + str(scaleH))
    roi = cv2.resize(roi, (1440, 900))
    
    cv2.imshow("Roi", roi)
    cv2.setMouseCallback('Roi', ce)

    key = cv2.waitKey(30)
    if key == 27:
        break

cv2.destroyAllWindows()

