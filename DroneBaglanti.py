from dronekit import connect #bu kod sayesinde python ile simulasyon ortamindaki ihamizi baglayabiliriz

drone = connect('127.0.0.1:14550',wait_ready=True) 
#'127.0.0.1:14550'=buradaki ifade simulasyonumuzun calistigi port
#wait_ready=True->bu ifade sayesinde bu kod yazilan porta baglanana kadar denenmeye devam edecektir

print(f"Drone arm durumu:{drone.armed}")
#dronun arm olup olmadigini bize True veya False olarak dondurecektir

print(f"Global frame{drone.location.global_frame}") 
#enlem,boylam ve deniz seviyesine gore irtifa
print(f"Global relative frame{drone.location.global_relative_frame}")
#enlem,boylam ve yerden yuksekligi

print(f"irtifa:{drone.location.global_frame.alt}")#sadece irtifa 
