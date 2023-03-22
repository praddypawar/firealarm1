from ast import arg
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


configData = config.Config()

def send_data(res_data):
    # print(res_data)
    try:
        channel_layer = get_channel_layer()
        for user in consumer.connected_user:
            async_to_sync(channel_layer.group_send)(user['user_group'], {
                        'type': 'site_config',
                        'response': res_data,
                    })
    except Exception as e:
        logging.info(f"GetAllSTatus1: {e}")

def get_New_Status():
    while True:
        time.sleep(1)
        print("main_data",len(config.main_data),config.main_data)
        if len(config.main_data) > 0:
            mydata = sonoff_opr.getDevices(config.main_data)
            print("get_New_Status")
            try:
                for i in mydata["devices"]:
                    print(i['name'],"----",i["status"])
            except:
                pass
            if config.user_details_status != mydata:
                config.user_details_status = mydata
                t1 = threading.Thread(target=send_data,args=(mydata,))
                t1.start()
                t1.join() 
                print("user_details_status")

  
# print("threading start")
# t2 = threading.Thread(target=get_New_Status)
# t2.start()
        
class Operations():
    def check_opr(self, res):
        with open(configData.userDetail,"r") as readFile:
            data = json.load(readFile)
        
        with open(configData.userStatus,"r") as readFile:
            statusData = json.load(readFile)

        if res["opr"] == "service":
            if res["opr_type"] == "login":
                print("Login New User")
                logging.info("New User Login...")
                
                for i in data:
                    if i["userEmail"]==res["record"]["userEmail"] and i["userPass"]==res["record"]["userPass"]:
                        config.main_data = i
                        mydata = sonoff_opr.getDevices(i)
                        # res_data = {
                        #     "status":"Login Successfylly",
                        #     "data":mydata
                        # }
                        print("------------;;;;")
                        if config.user_details_status != mydata:
                            config.user_details_status = mydata
                        print(mydata)
                        print("------------;;;;")
                        t1 = threading.Thread(target=send_data,args=(mydata,))
                        t1.start()
                        t1.join()     

            elif res["opr_type"] == "operation":
                for i in statusData:
                    if int(i["id"]) == int(res["record"]["id"]):
                        mydata = sonoff_opr.alram_opr(i,res["opr_param"],i["id"])
                        # res_data = {
                        #     "status":"oparation Successfully",
                        #     "data":mydata
                        # }
                        t1 = threading.Thread(target=send_data,args=(mydata,))
                        t1.start()
                        t1.join()  
