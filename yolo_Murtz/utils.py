# from yolodemo import *


####### Basic Hello drone #######

import time
import numpy as np
import dronekit_sitl
# sitl = dronekit_sitl.start_default()
# connection_string = sitl.connection_string()

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import argparse

###Variables###
w,h = 360,240
pid = [0.5,0.45,0.001]
Vx,Vy,Vz = 0,0,0
fbRange = [6200,6800]
pitch_errorSum = 0
yaw_errorSum = 0

def connectMyCopter():
    """
    To connect copter to script
    """
    parser = argparse.ArgumentParser(description='commands')
    parser.add_argument('--connect') #used in terminal like '--connect 127.0.0.1:14550'
    args = parser.parse_args()

    connection_string = args.connect
    sitl = None

    #Start SITL if no connection string specified
    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()


    print("Connecting to vehicle on: %s" % (connection_string))
    vehicle = connect(connection_string, wait_ready=True)

    return vehicle


# # Vehicle attributes (state)
# print("Get some vehicle attribute values:")
# print(" GPS: %s" % vehicle.gps_0)
# print(" Battery: %s" % vehicle.battery)
# print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
# print(" Is Armable?: %s" % vehicle.is_armable)
# print(" System status: %s" % vehicle.system_status.state)
# print(" Mode: %s" % vehicle.mode.name)    # settable


def arm_and_takeoff(vehicle, aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


def set_velocity_body(vehicle,Vx,Vy,Vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        Vx, Vy, Vz, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored)

    vehicle.send_mavlink(msg)
    vehicle.flush() #to sure that the command is sent to the drone without delay and takes effect immediately




def track_person(vehicle, info, w, pid, pPitch_Error, pYaw_Error):
    """
    Track a person based on obj detection
    """
    area = info[1]

    ##PID for Yaw
    yaw_error = info[0][0] - w // 2  #w/2 is the centre of the screen
    yaw_errorSum = yaw_errorSum + yaw_error
    yaw_speed = pid[0] * yaw_error + pid[1] * (yaw_error - pYaw_Error) + pid[2] * yaw_errorSum
    yaw_speed = int(np.clip(yaw_speed, -100,100))  #to limit val. Vals outside are clipped to interval edges.


    ##PID for Pitch
    if area > fbRange[0] and area < fbRange[1]:
        #Vx = 0
        pitch_error = 0 
        pPitch_Error = 0
    elif area < fbRange[0]:  #drone is too far
        pitch_error = info[1] - fbRange[0]
    elif area > fbRange[1]:  #drone is too close
        pitch_error = info[1] - fbRange[1]
    
    pitch_errorSum = pitch_errorSum + pitch_error
    pitch_speed = pid[0] * pitch_error + pid[1] * (pitch_error - pPitch_Error) + pid[2] * pitch_errorSum
    pitch_speed = int(np.clip(pitch_speed, -5, 5))


    #Setting the velocities 
    if info[0][0] != 0:
        Vx = pitch_speed
        Vy = yaw_speed
    else:
        Vx, Vy, Vz = 0
        pitch_error = 0
        yaw_error = 0

    print(Vx,Vy)
    #set_velocity_body(Vx, Vy, Vz)

    return pitch_error,yaw_error



#arm_and_takeoff(10)

# print("Returning to Launch")
# vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
# vehicle.close()

# # Shut down simulator if it was started
# if sitl:
#     sitl.stop()
#     print("Completed")