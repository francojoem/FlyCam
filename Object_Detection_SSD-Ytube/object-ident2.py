import cv2
import time

#thres = 0.45 # Threshold to detect object

#classNames = "person" - ERROR- why?
classFile = "E:/Drone_prg/Object_Detection_SSD-Ytube/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "E:/Drone_prg/Object_Detection_SSD-Ytube/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "E:/Drone_prg/Object_Detection_SSD-Ytube/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, draw=True, objects=[]):
    
    times, times_2 = [], []

    t1 = time.time()
   
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    t2 = time.time()

    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            #className = classNames[classId - 1]
            if classId-1 < len(classNames):
                className = classNames[classId - 1]
            else:
                className = "Unknown"

            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,0,255),thickness=2)
                    cv2.putText(img,classNames[classId-1],(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                    #counter+=1

                    times.append(t2-t1)
                    times = times[-20:]
                    ms = sum(times)/len(times)*1000
                    fps = 1000 / ms
                    print("FPS:",round(fps,2))
                    #fps = 1.0/(time.time() - start_time) #calculation of fps
                    cv2.putText(img, str(round(fps,2)), (0,30), cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255),2)
                    #print("Avg fps = ",fps/counter) # counter/(time.time() - start_time)
    return img,objectInfo


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)


    while True:
        success, img = cap.read()
        
        result, objectInfo = getObjects(img,0.45,0.2)
        #print(objectInfo)
        cv2.imshow("Output",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
