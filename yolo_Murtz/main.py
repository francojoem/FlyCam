###Tip - use Ctrl+? to comment out selected text

from utils import *
from yolodemo import *
import cv2

# vehicle = connectMyCopter()
# arm_and_takeoff(vehicle, 10)

while True:
    ##1- detect person
    img, info = findObjects(outputs, img)
    print("Center", info[0], "Area", info[1])

    ##2- track person
    pPitch_Error, pYaw_Error = track_person( info, w, pid, pPitch_Error, pYaw_Error)
    

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
