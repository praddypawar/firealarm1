# from SonoffBasic.sonoff import Sonoff

# while True:
#     print("-"*15,"Menu","-"*15)
#     print("1. Login")
#     print("2. Get Devices status")
#     print("3. On devices")
#     print("4. Off Devices")
#     print("5. Exit")
#     print("-"*25)
#     choice = int(input("Enter The choice: "))
#     if choice == 1:
#         pass
#     if choice ==2:
#         sonoff = Sonoff(username="ashaelesservice@gmail.com",password="75487548", region="as")
#         print(sonoff.devices) 

#     if choice ==3:
#         sonoff = Sonoff(username="ashaelesservice@gmail.com",password="75487548", region="as")
#         status_data = sonoff.change_device_status(deviceid ="1000f2434e",new_status = "on")

#     if choice ==4:
#         sonoff = Sonoff(username="ashaelesservice@gmail.com",password="75487548", region="as")
#         status_data = sonoff.change_device_status(deviceid ="1000f2434e",new_status = "off") 

#     if choice ==5:
#         break        
# import sonoff
from alarm import sonoff
s = sonoff.Sonoff("ashaeles@gmail.com", "75497549", "as")
devices = s.get_devices()
print(devices)