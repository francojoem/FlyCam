import cv2
from yolodemo import *

# Initialize CUDA
cv2.cuda.setDevice(0)

# Load the YOLO model
net = cv2.dnn.readNetFromDarknet("yolov4.cfg", "yolov4.weights")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Set the input image size
whT = 416 # Replace whT with an integer value that represents the width and height of the input image

# Set the mean values
net.setMean(0, 0, 0)

# Set the swapRB flag
net.setSwapRB(True)

while True:
 ########## 1- detect person ##########
 success, img = cap.read()

 # Convert the image to a blob
 blob = cv2.dnn.blobFromImage(img, scalefactor=1.0 / 255, size=(whT, whT), mean=(0, 0, 0), swapRB=True, crop=False)

 # Forward the blob through the network
 outputs = net.forward(["yolo_139", "yolo_150", "yolo_161"])

 # Find the objects in the output
 img, info = findObjects(outputs, img)

 # Print the center and area of each object
 for i in range(len(info)):
    print("Center", info[i][0], "Area", info[i][1])




 ########## 2- track person ##########
 pPitch_Error, pYaw_Error = track_person(info, w, pid_pitch, pid_yaw, pPitch_Error, pYaw_Error)
 

 cv2.imshow('Image', img)
 if cv2.waitKey(1) & 0xFF == ord('q'): 
    break

cap.release()
cv2.destroyAllWindows()
