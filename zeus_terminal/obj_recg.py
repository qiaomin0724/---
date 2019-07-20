#coding=utf-8
import numpy as np
import cv2
import time


class ObjectDetection:
    def __init__(self):
        self.prototxt = 'model/MobileNetSSD_deploy.prototxt.txt'  # Caffe 'deploy' prototxt file
        self.model = 'model/MobileNetSSD_deploy.caffemodel'  # Caffe pre-trained model
        self.pre_confidence = 0.4
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                   "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                   "sofa", "train", "tvmonitor"]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
        # 加载模型，预处理图片
        print("加载模型...")
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)

        pass


    def detection(self, input_image):
        self.image = input_image
        (h, w) = self.image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(self.image, (300, 300)), 0.007843, (300, 300), 127.5)
        # 执行物体检测
        #print("执行物体检测...")
        self.net.setInput(blob)
        detections = self.net.forward()
        all=[]
        # loop over the detections
        print detections.shape[2]
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]
            (startX, startY, endX, endY)=(0,0,0,0)
            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > self.pre_confidence:
                all.append([startX, startY, endX, endY])
                # extract the index of the class label from the `detections`,
                # then compute the (x, y)-coordinates of the bounding box for
                # the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                # display the prediction
                label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence * 100)
                cv2.rectangle(self.image, (startX, startY), (endX, endY),
                              self.COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                if label=='dog':
                    cv2.putText(self.image, "dog", (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)
        # show the output image
        #cv2.imshow("Output", self.image)
        # cv2.imwrite('Output',image)
        #cv2.waitKey(0)
        return len(all),self.image


if __name__ == '__main__':
    od = ObjectDetection()
    output = od.detection()
    print(output)
