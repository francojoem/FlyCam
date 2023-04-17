
# from yolodemo import *
# fbRange = [6200,6800]

####### Basic Hello drone #######

import time
import dronekit_sitl
# sitl = dronekit_sitl.start_default()
# connection_string = sitl.connection_string()

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import argparse



# def connectMyCopter():
#     """
#     To connect copter to script
#     """
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
    
    #return vehicle

    
# # Vehicle attributes (state)
# print("Get some vehicle attribute values:")
# print(" GPS: %s" % vehicle.gps_0)
# print(" Battery: %s" % vehicle.battery)
# print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
# print(" Is Armable?: %s" % vehicle.is_armable)
# print(" System status: %s" % vehicle.system_status.state)
# print(" Mode: %s" % vehicle.mode.name)    # settable


def arm_and_takeoff(aTargetAltitude):
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

def set_velocity_body(Vx,Vy,Vz):
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




def track_person(vehicle, info, w, pid, pError):
    """
    Track a person based on obj detection
    """
    area = info[1]
    x,y = info[0]
    
    error = x-w//2 #w/2 is the centre
    
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area < fbRange[0]:
        fb = 20
    elif area > fbRange[1]:
        fb = -20







arm_and_takeoff(10)

# print("Returning to Launch")
# vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator if it was started
if sitl:
    sitl.stop()
    print("Completed")