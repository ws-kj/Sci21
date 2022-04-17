import cv2
import numpy 
import urllib
import requests
import time
import sys
import socket

from globs import *
import eye

url = 'http://192.168.0.119/html/cam_pic.php' 

font = cv2.FONT_HERSHEY_SIMPLEX
fscale = 0.75
fcolor = (0, 255, 0)
fthick = 1

m_coord = (5, 20)
c_coord = (5, 45)

port = 11111
host = '192.168.0.119'

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

scount = 0;
sturn = 500;
sroi = True

def init_socket():
    socket.connect((host, port))
    socket.sendall(b'Connecting')
    
def init_cam():
    cv2.namedWindow('Camera', cv2.WND_PROP_FULLSCREEN) #no buttons
    cv2.setWindowProperty('Camera', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def cam_loop(cur_comm):
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
   
    width, height, depth = img.shape
#    scaleW = float(cv2.getWindowImageRect("Camera")[2])/float(width)
#    scaleH = float(cv2.getWindowImageRect("Camera")[3])/float(height)
    scaleW = float(480)/float(width)
    scaleH = float(320)/float(height)
    nx, ny = width*scaleW, height*scaleH
    #img = cv2.resize(img, nx, ny)

    cv2.namedWindow('Camera', cv2.WND_PROP_FULLSCREEN) #no buttons
    cv2.setWindowProperty('Camera', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Camera', img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        socket.close()
        sys.exit()

def process_input(com):
    print(com)
    if com == E_NONE:
        cur_comm = C_NONE
    elif com == E_UP:
        cur_comm = C_FORWARD
    elif com == E_LEFT:
        cur_comm = C_LEFT
    elif com == E_RIGHT:
        cur_comm = C_RIGHT
    elif com == E_BLINK:
        cur_comm = C_NONE
        
    return cur_comm

def send_data(cur_comm):
    msg = "{} {}".format(cur_mode, cur_comm)
    socket.sendall(bytes(msg, 'utf-8'))  

if __name__ == '__main__':

    eye.eye_cal()

    init_cam()
    init_socket()
    cur_mode = M_MOVE
    while 1:
        com = process_input(eye.eye_loop())
        cam_loop(com)
        send_data(com)
    cv2.destroyAllWindows()
    socket.close()
