import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firealarm.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from alarm import config
import json
from  alarm import sonoff_opr
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from firealarm import consumer
import threading
import logging
from alarm.views import user_site_config
from api.models import admins,client,devices,sharedevices
from alarm.sonoff import Sonoff




configData = config.Config()

def send_data(res_data,user_id):
    try:
        channel_layer = get_channel_layer()
        for user in consumer.connected_user:
            if f'live_user_{user_id}' == user['user_group']:
                async_to_sync(channel_layer.group_send)(f'live_user_{user_id}', {
                            'type': 'site_config',
                            'response': res_data,
                        })
    except Exception as e:
        logging.info(f"GetAllSTatus1: {e}")

# def get_New_Status():
#     while True:
#         time.sleep(1)
#         print("main_data",len(config.main_data),config.main_data)
#         if len(config.main_data) > 0:
#             mydata = sonoff_opr.getDevices(config.main_data)
#             print("get_New_Status")
#             try:
#                 for i in mydata["devices"]:
#                     print(i['name'],"----",i["status"])
#             except Exception as e:
#                 print("get_New_Status",e)
#             if config.user_details_status != mydata:
#                 config.user_details_status = mydata
#                 t1 = threading.Thread(target=send_data,args=(mydata,))
#                 t1.start()
#                 t1.join() 
#                 print("user_details_status")

def get_New_Status():
    while True:
        admin_lst = list(admins.objects.all().values("id","status","first_name","last_name","email","region","password"))
        for i in admin_lst:
            try:
                data = devices.objects.filter(admin_id=admins.objects.get(pk=i["id"]))
                db_devices_data = [{"deviceid": d.device_id, "status": d.device_status} for d in data]

                sonoff = Sonoff(username=i["email"],password=i["password"], region=i["region"])
                live_devices_data = sonoff.devices
                # print("live_devices_data---------",live_devices_data)
                live_devices_data1 = [{"deviceid": ld["deviceid"], "status": ld['status']} for ld in live_devices_data]

                db_devices_data = sorted(db_devices_data, key = lambda s: s['deviceid'])
                live_devices_data1 = sorted(live_devices_data1, key = lambda s: s['deviceid'])

                for li in live_devices_data1:
                    if li not in db_devices_data:
                        # print(li,"ooo")
                        if up_devices := devices.objects.filter(device_id=li["deviceid"]):
                            # print("len(up_devices:",len(up_devices))
                            
                            if len(up_devices) > 0:
                                up_devices[0].device_status = li["status"]
                                up_devices[0].save()

                                if sh_devices := sharedevices.objects.filter(device_pk=up_devices[0].pk):
                                    if len(sh_devices) >0:
                                        print(sh_devices[0].client_id.pk)
                                        cl_data = client.objects.get(pk=sh_devices[0].client_id.pk)
                                        data = Login(cl_data.email,cl_data.password)
                                        t1 = threading.Thread(target=send_data,args=(data,data[0]["client_data"]["id"],))
                                        t1.start()
            except Exception as e:
                print("Error get_New_Status: ",e)
                        
        time.sleep(1)

  
print("threading start")
t2 = threading.Thread(target=get_New_Status)
t2.start()
        



def Login(email,password):
    data =[]
    try:
        if client_data := list(client.objects.filter(email=email, password=password).values("id","status","cover_pic","first_name","last_name","address","phone","email","password")):
            devices_id = list(sharedevices.objects.filter(client_id=client_data[0].get("id",0)).values("device_pk").distinct())
            _devices_list=[]
            for device_id in devices_id:
                if device_list := list(devices.objects.filter(id=device_id.get("device_pk",0)).values("id","status","admin_id_id","name","device_id","device_status")):
                    if admin_data := list(admins.objects.filter(pk=device_list[0].get("admin_id_id",0)).values("id","status","first_name","last_name","email","region","password")):
                        device_list[0].update({"admin_detail":admin_data[0]})
                    _devices_list.append(device_list[0])
            data.append({"client_data":client_data[0],"devices_list":_devices_list})
    except Exception as e:
        print(e)
        # data[{"error": str(e)}]
    finally:
        return data

def Alarm_opr(admin_data,p):
    try:
        sonoff = Sonoff(username=admin_data.email,password=admin_data.password, region=admin_data.region)
        status_data = sonoff.change_device_status(deviceid = p[0],new_status = p[1])
        if status_data =="device is already off":
            if devies_data := devices.objects.filter(admin_id_id=admin_data,device_id=p[0])[0]:
                print(devies_data)
                devies_data.device_status = "off"
                devies_data.save()
        elif status_data =="status successfully changed to on":
            if devies_data := devices.objects.filter(admin_id_id=admin_data,device_id=p[0])[0]:
                print(devies_data)
                devies_data.device_status = "on"
                devies_data.save()
        elif status_data =="status successfully changed to off":
            if devies_data := devices.objects.filter(admin_id_id=admin_data,device_id=p[0])[0]:
                print(devies_data)
                devies_data.device_status = "off"
                devies_data.save()
        elif status_data == "device is already on":
            if devies_data := devices.objects.filter(admin_id_id=admin_data,device_id=p[0])[0]:
                print(devies_data)
                devies_data.device_status = "on"
                devies_data.save()
        return True
    except Exception as e:
        print(e)
        return False
    


class Operations():
    def check_opr(self, res):
        if res["opr"] == "service":
            if res["opr_type"] == "login":
                try:
                    print("login.....")
                    email = res["record"]["userEmail"]
                    password = res["record"]["userPass"]
                    data = Login(email,password)
                    t1 = threading.Thread(target=send_data,args=(data,data[0]["client_data"]["id"],))
                    t1.start()
                except Exception as e:
                    print(e)  

            elif res["opr_type"] == "operation":
                print("operation")
                try:
                    p = res["opr_param"].split("-")
                    admin_data =  admins.objects.get(pk=int(res["record"]["admin_id"]))
                    client_data= client.objects.get(pk=int(res["record"]["user_id"]))
                    Alarm_opr(admin_data,p)
                    data = Login(client_data.email,client_data.password)
                    t1 = threading.Thread(target=send_data,args=(data,data[0]["client_data"]["id"],))
                    t1.start()

                except admins.DoesNotExist as e:
                    print(e)

            # elif res["opr_type"] == "update":


        else:
            logging.error("Operations =>> response not found")


