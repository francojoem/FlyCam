import cv2
from yolodemo import *

# Initialize CUDA
cv2.cuda.setDevice(0)

# Load the YOLO model
net = cv2.dnn.readNetFromDarknet("yolov4.cfg", "yolov4.weights")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
#net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
#net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Create a model object from the net object
model = cv2::dnn::Model(net)

# Set the input image size
model.setInputSize(whT, whT)

# Set the input scale factor
model.setInputScale(1.0 / 255)

# Set the mean values
model.setMean(0, 0, 0)

# Set the swapRB flag
model.setSwapRB(True)

# Define the video capture object
cap = cv2.VideoCapture(0) # Use 0 for webcam or a video file name

while True:
    ########## 1- detect person ##########
    success, img = cap.read()

    # Convert the image to a blob
    blob = cv2.dnn.blobFromImage(img, 1.0 / 255, (whT, whT), (0, 0, 0), 1, crop=False)

    # Forward the blob through the model
    outputs = model.forward(["yolo_139", "yolo_150", "yolo_161"])

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
