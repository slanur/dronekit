from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import math

iha = connect("127.0.0.1:14550",wait_ready=True)

# Connect to the iha
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


def send_ned_position(north, east, down):
    msg = iha.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111111000,
        north, east, down,
        0, 0, 0,
        0, 0, 0,
        0, 0
    )
    iha.send_mavlink(msg)
    iha.flush() #bbu bir komutun mavlink'e hemen g,nderilmesini saglar


arm_Ol_ve_yuksel(5)

radius = 2  # yaricap
steps = 36  # cember 10 derece araliklarla 36 parcaya bolundu
height = -5  # yerden 5 metre yuksekte

print("cember manevrasina baslaniyor...")
for i in range(steps + 1):
    angle = (2 * math.pi / steps) * i #Burada her nokta için açı (radyan cinsinden) hesaplanır.

    north = radius * math.cos(angle) 
    east = radius * math.sin(angle)
    #bu iki satirda aslinda cemberin 2D duzleminde gidebilecegi noktalar belirleniyor. (north, east)=(r⋅cos(θ),r⋅sin(θ))

    send_ned_position(north, east, height)
    time.sleep(0.5)

print("camber tamamlandi. Landing...")
iha.mode = VehicleMode("LAND")

while iha.armed:
    print(f" inis yapiliyor... yukseklik: {iha.location.global_relative_frame.alt:.2f}")
    time.sleep(1)

print("inis yapildi ve disarm yapildi.")
iha.close()