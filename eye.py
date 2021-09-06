import cv2
import numpy as np

from globs import *

cap = cv2.VideoCapture(0)

width = cap.get(3)
height = cap.get(4)

def eye_loop():
    ret, frame = cap.read()
#    if ret is False: 
#        return E_NONE

    roi = cv2.flip(frame, 1)
#   roi = frame[235: 250, 325: 356]
    rows, cols, _ = roi.shape
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)

    _, threshold = cv2.threshold(gray_roi, 65, 255, cv2.THRESH_BINARY_INV)

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

#        print(ret)

        break

#    cv2.imshow("Threshold", threshold)
#    cv2.imshow("gray roi", gray_roi)
#    cv2.imshow("Roi", roi)
    return ret

cv2.destroyAllWindows()

