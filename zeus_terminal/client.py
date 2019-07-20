#!usr/bin/python
# coding=utf-8

import socket
import cv2
import numpy


# 接受图片大小的信息
def recv_size(sock, count):
    buf = ''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


# socket.AF_INET 用于服务器与服务器之间的网络通信
# socket.SOCK_STREAM 代表基于TCP的流式socket通信
if __name__=='__main__':
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 连接服务端
	address_server = ('192.168.0.149', 9999)
	print 'connecting'
	sock.connect(address_server)
	print 'connected!'
	while True:
	    length = recv_size(sock, 16)  # 首先接收来自客户端发送的大小信息
	    if len(length) == 16:  # 若成功接收到大小信息，进一步再接收整张图片
		stringData = recv_size(sock, int(length))
		data = numpy.fromstring(stringData, dtype='uint8')
		decimg = cv2.imdecode(data, 1)  # 解码处理，返回mat图片
		img = cv2.resize(decimg, (640, 480))
		cv2.imshow('SERVER', img)
		if cv2.waitKey(1) == 27:
		    break
	    # print('Image recieved successfully!')



	sock.close()
	cv2.destroyAllWindows()





