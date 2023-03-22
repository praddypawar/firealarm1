from alarm.sonoff import Sonoff
from alarm import config
import time

def getDevices(data):
    print(data["userEmail"],data["userPass"],data["userRegion"])
    sonoff = Sonoff(username=data["userEmail"],password=data["userPass"], region=data["userRegion"])
    config.loginuserlist.append({"id":data["id"],"sonoff":sonoff})
    devices = sonoff.devices
    print(devices,"devices")
    return {"id": data["id"], "userEmail": data["userEmail"], "userPass": data["userPass"], "userRegion": data["userRegion"], "devices": devices}

def getDevices_status(data):
    # print(data["userEmail"],data["userPass"],data["userRegion"])
    sonoff = Sonoff(username=data["userEmail"],password=data["userPass"], region=data["userRegion"])
    # config.loginuserlist.append({"id":data["id"],"sonoff":sonoff})
    devices = sonoff.devices
    get_data = {
        "id":data["id"],
       "userEmail":data["userEmail"],
       "userPass":data["userPass"],
       "userRegion":data["userRegion"],
       "devices":devices
    }
    return get_data

def opr(data,param):
    print(data,param)
    p = param.split("-")
    print(p)
    sonoff = Sonoff(username=data["userEmail"],password=data["userPass"], region=data["userRegion"])
    # devices = sonoff.devices
    status_data = sonoff.change_device_status(deviceid = p[0],new_status = p[1])
    get_data = {
        "id":data["id"],
        "userEmail":data["userEmail"],
        "userPass":data["userPass"],
        "userRegion":data["userRegion"],
        "devices":status_data
    }
    return get_data


def alram_opr(data,param,id):
    p = param.split("-")
    print(p)
    sonoff = Sonoff(username=data["userEmail"],password=data["userPass"], region=data["userRegion"])
    status_data = sonoff.change_device_status(deviceid = p[0],new_status = p[1])
    print(status_data,"++++")
    if status_data =="device is already off":
        for i in data["devices"]:
            if i["deviceid"] == p[0]:
                i["status"] ="off"

    elif status_data =="status successfully changed to on":
        for i in data["devices"]:
            if i["deviceid"] == p[0]:
                i["status"] ="on"

    elif status_data =="status successfully changed to off":
        for i in data["devices"]:
            if i["deviceid"] == p[0]:
                i["status"] ="off"
    
    return data


def alram_opr_db(data,param,id):
    p = param.split("-")
    print(p)
    sonoff = Sonoff(username=data["userEmail"],password=data["userPass"], region=data["userRegion"])
    status_data = sonoff.change_device_status(deviceid = p[0],new_status = p[1])
    print(status_data,"++++")
    for i in data["devices"]:
        if status_data == "device is already off" and i["deviceid"] == p[0] or status_data != "device is already off" and status_data != "status successfully changed to on" and status_data == "status successfully changed to off" and i["deviceid"] == p[0]:
            i["status"] ="off"

        elif status_data != "device is already off" and (status_data != "status successfully changed to on" or i["deviceid"] == p[0]) and (status_data == "status successfully changed to on" or status_data != "status successfully changed to off") and status_data == "status successfully changed to on":
            i["status"] ="on"

    return data        
