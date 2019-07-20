import numpy as np
import cv2
import time


# 调用摄像头拍摄一张图片
cap = cv2.VideoCapture(0)
ret, image = cap.read()
cv2.imshow('frame', image)
cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()


# 初始化一些变量
# image = cv2.imread('./our_testSet/02.jpg')       # 输入图片
prototxt = 'MobileNetSSD_deploy.prototxt.txt'    # Caffe 'deploy' prototxt file
model = 'MobileNetSSD_deploy.caffemodel'     # Caffe pre-trained model
pre_confidence = 0.2
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# 加载模型，预处理图片
print("加载模型...")
net = cv2.dnn.readNetFromCaffe(prototxt, model)
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

# 执行物体检测
print("执行物体检测...")
net.setInput(blob)
detections = net.forward()

# loop over the detections
for i in np.arange(0, detections.shape[2]):
	# extract the confidence (i.e., probability) associated with the
	# prediction
	confidence = detections[0, 0, i, 2]

	# filter out weak detections by ensuring the `confidence` is
	# greater than the minimum confidence
	if confidence > pre_confidence:
		# extract the index of the class label from the `detections`,
		# then compute the (x, y)-coordinates of the bounding box for
		# the object
		idx = int(detections[0, 0, i, 1])
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

		# display the prediction
		label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
		print("[INFO] {}".format(label))
		cv2.rectangle(image, (startX, startY), (endX, endY),
			COLORS[idx], 2)
		y = startY - 15 if startY - 15 > 15 else startY + 15
		cv2.putText(image, label, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)


# show the output image
cv2.imshow("Output", image)
#cv2.imwrite('Output',image)
cv2.waitKey(0)
