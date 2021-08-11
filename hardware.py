from globs import *

def command(m, c):
    if c == C_FORWARD:
        if m == M_MOVE:
            c_forward()
    elif c == C_LEFT:
        if m == M_MOVE:
            c_left()
        elif m == M_RAISE:
            c_lower()
        elif m == M_EXTEND:
            c_retract()
    elif c == C_RIGHT:
        if m == M_MOVE:
            c_right()
        elif m == M_RAISE:
            c_raise()
        elif m == M_EXTEND:
            c_extend()

def c_forward():
    pass

def c_left():
    pass

def c_right():
    pass

def c_lower():
    pass

def c_raise():
    pass

def c_retract():
    pass

def c_extend():
    pass
