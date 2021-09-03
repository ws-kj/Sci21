import cv2
import numpy as np

cap = cv2.VideoCapture(0)

width = cap.get(3)
height = cap.get(4)

while True:
    ret, frame = cap.read()
    if ret is False: 
        break
    
    roi = cv2.flip(frame, 1)
#    roi = frame[235: 250, 325: 356]
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


        ml = width/3
        mr = ml * 2

        if w > 3*h:
            print("CLOSED")
        else:
            if cx < ml:
             print("LEFT")
            if cx > mr:
                print("RIGHT")

        break

#    cv2.imshow("Threshold", threshold)
#    cv2.imshow("gray roi", gray_roi)
    cv2.imshow("Roi", roi)
    key = cv2.waitKey(30)
    if key == 27: 
        break

cv2.destroyAllWindows()

