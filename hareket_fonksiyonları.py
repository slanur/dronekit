from dronekit import connect
from pymavlink import mavutil
import time
 
iha = connect("127.0.0.1:14550",wait_ready=True)

#kalkis noktasini referans alan hareket fonksiyonu
def goto_position_target_local_ned(north,east,down):
    """
    Send SET_POSITION_TARGET_LOCAL_NED command the request the iha fly to a specified
    location in the North, East, Down frame.
    """
    msg = iha.message_factory.set_position_target_local_ned_encode(
    0,       # time_boot_ms (not used)
    0, 0,    # target_system, target_component
    mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
    0b0000111111111000, # type_mask (only speeds enabled)
    north, east, down, # x, y, z positions
    0, 0, 0, # x, y, z velocity in m/s
    0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
    0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
# send command to drone
    iha.send_mavlink(msg)

# goto_position_target_local_ned(5,5,-1) #kuzeye 5,  doguya 5 ve yukari yonde 1
# #baslangic noktasina gore olan bu noktaya hareket ediyor

#istenilen hiza gore belirli sure hareket fonksiyonu
def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move iha in direction based on specified velocity vectors.
    """
    msg = iha.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)


    # send command to iha on 1 Hz cycle
    for x in range(0,duration):
        iha.send_mavlink(msg)
        time.sleep(1)

# send_ned_velocity(5,0,-1,5)

#drone'un acisini degistiren fonksiyon 
def condition_yaw(heading, relative=False):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = iha.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to iha
    iha.send_mavlink(msg)

condition_yaw(180, True)