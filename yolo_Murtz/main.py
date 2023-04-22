###Tip - use Ctrl+? to comment out selected text

from utils import *
from yolodemo import *
import cv2

pPitch_Error = 0
pYaw_Error = 0

# vehicle = connectMyCopter()
# arm_and_takeoff(vehicle, 10)

while True:
    ########## 1- detect person ##########
    success, img = cap.read()
    #start_time = time.time()

    blob = cv2.dnn.blobFromImage(img,1/255,(whT,whT),[0,0,0],1,crop=False)#network cannot handle plain img
    #Need to be converted into 'blob'
    net.setInput(blob)

    layerNames = net.getLayerNames() #names of all layers in network
    #print(layerNames)
    outindex = [[i] for i in net.getUnconnectedOutLayers()]
    outTensor = np.array(outindex) #just using net.getUnconnectedOutLayers() was not working; so converted into tensor
    #print(outTensor)
    outputNames = [layerNames[i[0]-1] for i in outTensor] #gives ['yolo_139', 'yolo_150', 'yolo_161']

    outputs = net.forward(outputNames) #gives (507, 85) (8112, 85) (2028, 85)
    
    img, info = findObjects(outputs, img)
    print("Center", info[0], "Area", info[1])




    ########## 2- track person ##########
    pPitch_Error, pYaw_Error = track_person( info, w, pid_pitch, pid_yaw, pPitch_Error, pYaw_Error)
    

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()




# print("Returning to Launch")
# vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
# vehicle.close()

# # Shut down simulator if it was started
# if sitl:
#     sitl.stop()
#     print("Completed")
