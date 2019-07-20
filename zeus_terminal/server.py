# -*-coding:utf-8 -*-
import socket
import threading
import cv2
import numpy
import flask
from flask import Flask,render_template
from time import sleep
from obj_recg import *
app=Flask(__name__)
img_l=[]
num=0
falls=0
@app.route('/')
def Ret_Data():
        return 'asdasd'

def recv_all(sock, count):
    buf = ''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


threadLock = threading.Lock()

videoDatastr = ''

conn_list = []
def robotVideoThread(sock):
    while True:
        try:
            global videoDatastr
            conn, addr = sock.accept()
            print('robot Connected with' + ' ' + addr[0] + ':' + str(addr[1]))
            conn_list.append(conn)
            dect = ObjectDetection()
            while True:
                length = recv_all(conn, 16)
                if len(length) == 16:
                    videoDatastr = recv_all(conn, int(length))
                    data = numpy.fromstring(videoDatastr, dtype='uint8')
                    decimg = cv2.imdecode(data, 1)
                    img_l=decimg[0:240,320:640]
                    rect,img=dect.detection(img_l)
                    num=rect
                    print num
                    cv2.imshow('img', img)
                    if cv2.waitKey(1) == 27:
                        break
        except:
            continue

if __name__ == '__main__':

    s_robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('', 8889)
    s_robot.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_robot.bind(address)
    s_robot.listen(True)
    print('robot initiated')
    threading.Thread(target=robotVideoThread, args=(s_robot, )).start()
    app.run(host='192.168.0.149',port=8989,debug=False)

