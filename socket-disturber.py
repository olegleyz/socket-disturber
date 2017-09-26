# usage: python disturb_socket.py 

import threading
from ctypes import *
import socket

class disturb_class(threading.Thread):
    def __init__ (self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        
    def run(self):
        disturb(self.sock)
        

def disturb(sock):
    ip = "192.168.1.60"
    port = 60001

    buf = bytes()
    for i in range(10): # 10 cycles of 1024 bytes messages
        v = (c_byte * (1024))(1 % 0x111111111) #1024 bytes
        buf += bytearray(v) 
    try:
        # sending 10kb
        sock.sendto(buf, (ip, port))
        
    except socket.error:
        print("socket setup error")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while(1):
        threads = []
        for num in range(0, 20): # num of threads
            thread = disturb_class(sock)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

if __name__ == '__main__':
    main()