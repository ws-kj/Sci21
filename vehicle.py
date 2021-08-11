import socket

import globs

host = '192.168.0.111'
port = 11111

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def init_socket():
    s.bind((host, port))
    s.listen(1)
    print("Server listening on 11111...")

def poll_socket():
    while True:
        conn, addr = s.accept()
        try:
            print('conn from ', addr)
            while True:

                data = conn.recv(1024)
                if data:
                    arr = data.decode().split(' ')
                    if len(arr) > 1:
                        mode = int(arr[0])
                        comm = int(arr[1])
                        print(mode, comm)
        finally:
            conn.close()

if __name__ == '__main__':
    init_socket()
    while True:
        poll_socket()


