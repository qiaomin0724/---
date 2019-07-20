#!/usr/bin/python
# -*-coding:utf-8 -*-
import socket
import cv2
import numpy
from time import sleep
if __name__=='__main__':
	while True:
		print "Connecting"
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			address_server = ('192.168.0.149', 8889)
			sock.connect(address_server)
			capture = cv2.VideoCapture(0)
			ret, frame = capture.read()
			encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
			while ret:
				ret, frame = capture.read()
				cv2.resize(frame, (640, 480))
				img_encode = cv2.imencode('.jpg', frame, encode_param)[1]
				data = numpy.array(img_encode)
				stringData = data.tostring()
				sock.sendall(str(len(stringData)).ljust(16))
				sock.sendall(stringData)
				sleep(0.5)
			sock.close()
			cv2.destroyAllWindows()
		except:
			sleep(1)
			continue
