from dronekit import connect,VehicleMode,LocationGlobalRelative
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

arm_Ol_ve_yuksel(10)