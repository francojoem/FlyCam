import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
whT = 416
confThreshold = 0.5
nmsThreshold = 0.3


classesFile = 'coco.names'
classNames = []
with open(classesFile,'rt') as f:
    classNames = f.read().split('\n')
# print(classNames)
# print(len(classNames))

modelConfiguration = 'yolov4.cfg'
modelWeights = 'yolov4.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


def findObjects(outputs,img):
    """
    to find objs that have bboxes with high conf 
    and add them to a list 
    
    """

    hT,wT,cT = img.shape #org dimensions of image
    #when good obj detcn occurs, will put values of that box in following lists-
    bbox = [] #will contain x,y,w and h
    classIds = []
    confs = [] #conf values
    listC = [] #list of centres of all persons that're detected
    listArea = [] #list of areas of all persons detected
    #info = []

    for output in outputs:
        for det in output:
            scores = det[5:] #remove first five which are x, y, etc.
            classId = np.argmax(scores) #to find index of class iwth max value
            confidence = scores[classId] #save conf level
            if confidence > confThreshold:
                w,h = int(det[2]*wT), int(det[3]*hT) #det[2] is a percentage, so we've to multiply with actual W and H
                x,y = int((det[0]*wT)-w/2), int((det[1]*hT)-h/2) #this is x and y of center
                #which we got by multpying x% with W and subtr w/2

                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))

    #print(len(bbox))

    indices = cv2.dnn.NMSBoxes(bbox,confs,confThreshold,nmsThreshold) #NMS- to remove overlapping bboxes
    #NMS- Non-maximum Suppression
    # print(indices)


    for i in indices:
        box = bbox[i]
        x,y,w,h = box [0],box[1],box[2],box[3]

        cx = x + w // 2  #centre of bbox; for face tracking
        cy = y + h // 2
        area = w * h

        listC.append([cx, cy])
        listArea.append(area)
        #info.append([listC,listArea])

        #print(cx, cy, area)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255),
                      2)  #BGR color format
        cv2.circle(img, (cx, cy), 5, (255, 0, 0),
                   cv2.FILLED)  #to plot circle at the centre of bbox

        #because of- 'IndexError: list index out of range'
        try:
            cv2.putText(
                img, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%',
                (x, y),
                cv2.FONT_HERSHEY_
