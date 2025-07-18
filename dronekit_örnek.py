#Drone’u kaldırın 2 metreye kaldırın. 
# #5 metre kuzeye götürün. İndirin tekrar bu sefer 10 metreye kaldırın.
#  4 metre kuzey batıya götürün indirin. 
# Tekrar kaldırın Return to rtl modunu aktive edin. 
# Drone modu tamamlayınca disarm edin.

from dronekit import connect,VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

iha = connect("127.0.0.1:14550",wait_ready=True)

def arm_Ol_ve_yuksel(hedef_yukseklik):
    while (iha.is_armable is not True):
        print("Iha arm edilebilir durumda degil")
        time.sleep(1)
    print("Iha arm edilebilir")

    iha.mode = VehicleMode("GUIDED")
    while iha.mode.name != 'GUIDED':
        print("GUIDED moduna gecis yapiliyor")
        time.sleep(1)
    print("GUIDED moduna gecis yapildi")
    iha.armed = True
    while (iha.armed is not True):
        print("IHA arm ediliyor!!!")
        time.sleep(1)
    print("IHA arm edildi")

    iha.simple_takeoff(hedef_yukseklik)
    print("IHA hedefe yukseliyor")
    while (iha.location.global_relative_frame.alt< hedef_yukseklik*0.9):
        print(f"IHA'nin suan ki yuksekligi:{iha.location.global_relative_frame.alt}")
        time.sleep(1)
    print("IHA belirlenen yukseklige ulasti")


def goto_position_target_local_ned(north,east,down):
    msg = iha.message_factory.set_position_target_local_ned_encode(
    0,       
    0, 0,    # target_system, target_component
    mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
    0b0000111111111000, 
    north,east,down, # x, y, z positions
    0, 0, 0, 
    0, 0, 0, 
    0, 0)    
    iha.send_mavlink(msg)
    time.sleep(3)
    
def inis_yap():
    print("inis baslatiliyor")
    iha.mode = VehicleMode("LAND")
    while iha.armed:
        print(f"İniyor. Yukseklik: {iha.location.global_relative_frame.alt}")
        time.sleep(1)
    print("İHA indi ve disarm oldu.")

print("Iha 2 metre yukseliyor")
arm_Ol_ve_yuksel(2)

print("Drone 5m kuzeye goturuluyor")
goto_position_target_local_ned(5,0,-2)
time.sleep(2)

print("indiriliyor")
inis_yap()
time.sleep(2)

print("10 metreye kaldiriliyor")
arm_Ol_ve_yuksel(10)
time.sleep(2)

print("4 metre kuzey batiya goturuluyor")
goto_position_target_local_ned(4,-4,-10)
time.sleep(2)

print("indiriliyor")
inis_yap()
time.sleep(2)

print("tekrar kaldiriliyor")
arm_Ol_ve_yuksel(2)
time.sleep(2)

inis_yap()
print("Gorev tamamlandi")
