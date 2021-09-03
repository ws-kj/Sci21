import cv2
import numpy 
import urllib
import requests
import time
import sys
import socket

from globs import *
import eye

url = 'http://192.168.0.111/html/cam_pic.php' 

cur_mode = M_MOVE
cur_comm = C_NONE

font = cv2.FONT_HERSHEY_SIMPLEX
fscale = 0.75
fcolor = (0, 255, 0)
fthick = 1

m_coord = (5, 20)
c_coord = (5, 45)

port = 11111
host = '192.168.0.111'

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def init_socket():

    while True:
        try:
            urllib.request.urlopen('http://google.com')
            print("connected to internet")
            break
        except:
            time.sleep(1)
            continue

    socket.connect((host, port))
    socket.sendall(b'Connecting')
    
def init_cam():
    cv2.namedWindow('Camera', 16) #no buttons
    cv2.setWindowProperty('Camera', cv2.WND_PROP_FULLSCREEN, 1)

def cam_loop():
    resp = urllib.request.urlopen(url)
    img_arr = numpy.array(bytearray(resp.read()), dtype=numpy.uint8)
    img = cv2.imdecode(img_arr, -1)

    mode_text = ""
    comm_text = ""

    if cur_mode == M_MOVE:
        mode_text = "Move Mode"
    elif cur_mode == M_RAISE:
        mode_text = "Raise Mode"
    elif cur_mode == M_EXTEND:
        mode_text = "Expand Mode"

    if cur_comm == C_NONE:
        comm_text = "No Command"
    elif cur_comm == C_FORWARD:
        if cur_mode == M_MOVE:
            comm_text = "Move Forward"
        else:
            comm_text = "No Command"
    elif cur_comm == C_LEFT:
        if cur_mode == M_MOVE:
            comm_text = "Turn Left"
        elif cur_mode == M_RAISE:
            comm_text = "Lower Arm"
        elif cur_mode == M_EXTEND:
            comm_text = "Retract Arm"
    elif cur_comm == C_RIGHT:
        if cur_mode == M_MOVE:
            comm_text = "Turn Right"
        elif cur_mode == M_RAISE:
            comm_text = "Raise Arm"
        elif cur_mode == M_EXTEND:
            comm_text = "Extend Arm"
    
    img = cv2.putText(img, mode_text, m_coord, font, fscale, fcolor, fthick, cv2.LINE_AA)

    img = cv2.putText(img, comm_text, c_coord, font, fscale, fcolor, fthick, cv2.LINE_AA)

    img = cv2.flip(img, 1)  

    cv2.imshow('Camera', img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        sys.exit()

def process_input():
    pass

def send_data():
    msg = "{} {}".format(cur_mode, cur_comm)
    socket.sendall(bytes(msg, 'utf-8'))  

if __name__ == '__main__':
    init_cam()
    init_socket()
    while 1:
        process_input()
        eye_loop()
        send_data()
        cam_loop()
    cv2.destroyAllWindows()
    socket.close()
