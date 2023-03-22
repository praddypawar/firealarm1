from django.shortcuts import render,redirect,HttpResponse
import json
from  alarm import sonoff_opr
from django.contrib import messages


# Create your views here.

def index(request):
    return HttpResponse(json.dumps({"status": 200, "response": "Happy programming"}), content_type="application/json")

def operation(request):
    if request.method != "POST":
        return
    id_data = request.POST.get("id")
    opr_param = request.POST.get("opr_param")
    print(id_data, opr_param)
    with open("static/userDetail.json") as readFile:
        data = json.load(readFile)
    print(data[0], "====")
    for i in data:
        if int(i["id"]) == int(id_data):
            print(i, "----")
            mydata = sonoff_opr.opr(i, opr_param)
            return HttpResponse(json.dumps({"status": 200, "response": mydata}), content_type="application/json")

    return HttpResponse(json.dumps({"status_code": 400, "response": "Method Not Allow"}), content_type="application/json")

def userlogin(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"status_code": 400, "response": "Method Not Allow"}), content_type="application/json")

    userEmail = request.POST.get("userEmail")
    userPass = request.POST.get("userPass")
    with open("static/userDetail.json") as readFile:
        data = json.load(readFile)
    for i in data:
        if i["userEmail"] == userEmail and i["userPass"] == userPass:
            mydata = sonoff_opr.getDevices(i)
            res_data = {"status": "Login Successfylly", "data": mydata}
            return HttpResponse(json.dumps({"status_code": 200, "response": res_data}), content_type="application/json")

    return HttpResponse(json.dumps({"status_code": 200, "response": "Something Wrong"}), content_type="application/json")

def user_site_config():
    return {"id": 1, "userEmail": "ashaelesservice@gmail.com", "userPass": "75487548", "userRegion": "as"}



"""
[
    {
        "client_data": {
            "id": 1,
            "created_by": "system",
            "created_at": "2022-05-28T12:58:20.854046Z",
            "updated_by": "system",
            "updated_at": "2022-05-28T13:07:05.486161Z",
            "status": 1,
            "cover_pic": "media/webs/client/cover-pic/profile-pic-1-1653743225.jpg",
            "first_name": "nikhil",
            "last_name": "singh",
            "address": "pandesara",
            "phone": "3454567898",
            "email": "nikhil@gmail.com",
            "password": "123"
        },
        "devices_list": [
            {
                "id": 1,
                "created_by": "system",
                "created_at": "2022-05-31T19:30:50.086436Z",
                "updated_by": "system",
                "updated_at": "2022-05-31T19:34:17.278345Z",
                "status": 1,
                "admin_id_id": 3,
                "name": "1000f2c472 Zone 1 fire",
                "device_id": "1000f2c472",
                "device_status": "off",
                "admin_detail": {
                    "id": 3,
                    "created_by": "system",
                    "created_at": "2022-05-28T12:21:55.281521Z",
                    "updated_by": "system",
                    "updated_at": "2022-05-28T12:21:55.281521Z",
                    "status": 1,
                    "first_name": "kadir",
                    "last_name": "bhai",
                    "email": "ashaelesservice@gmail.com",
                    "region": "as",
                    "password": "75487548"
                }
            },
            {
                "id": 2,
                "created_by": "system",
                "created_at": "2022-05-31T19:30:50.111641Z",
                "updated_by": "system",
                "updated_at": "2022-05-31T19:34:17.292350Z",
                "status": 1,
                "admin_id_id": 3,
                "name": "Demi fire alarm ",
                "device_id": "10010ed8c5",
                "device_status": "off",
                "admin_detail": {
                    "id": 3,
                    "created_by": "system",
                    "created_at": "2022-05-28T12:21:55.281521Z",
                    "updated_by": "system",
                    "updated_at": "2022-05-28T12:21:55.281521Z",
                    "status": 1,
                    "first_name": "kadir",
                    "last_name": "bhai",
                    "email": "ashaelesservice@gmail.com",
                    "region": "as",
                    "password": "75487548"
                }
            }
        ]
    }
]

"""


from api.models import admins,client,devices,sharedevices


def UserLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # print(email,password)

        if admins.objects.filter(email=email,password=password).exists():
            admin_data = admins.objects.filter(email=email,password=password)[0]
            print("admin_data",admin_data)
            request.session["id"] = admin_data.id
            request.session["type"] = "admin"
            request.session["email"] = admin_data.email
            messages.success(request, 'Admin login successfully.')
            return redirect("dashboard")
        elif client.objects.filter(email=email,password=password).exists():
            client_data = client.objects.filter(email=email,password=password)
            print("client_data",client_data)
        


    return render(request,"login.html")

def Logout(request):
    if "id" in request.session:
        del request.session["id"]

    if "type" in request.session:
        del request.session["type"]

    if "email" in request.session:
        del request.session["email"]
    
    return redirect("userlogin")

def Dashboard(request):
    if "id" not in request.session and "type" not in request.session and "email" not in request.session:
        return redirect("userlogin")

    admin_data = admins.objects.get(pk=request.session["id"])
    total_client = client.objects.all().count()
    total_devices = devices.objects.all().count()
    total_sharedevices = sharedevices.objects.all().count()
    client_data = client.objects.all()
    payload = {"admin_data": admin_data, "client_data": client_data, "total_client": total_client, "total_devices": total_devices, "total_sharedevices": total_sharedevices}

    if request.method == "POST":
        coverpic = request.FILES["coverpic"]
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(fname,lname,address,phone,email,password)
        new_data = client(cover_pic=coverpic,first_name=fname,last_name=lname,address=address,phone=phone,email=email,password=password)
        new_data.save()
        messages.success(request, 'client data added.')
        # print("coverpic:= ",coverpic)
        return redirect("dashboard")

    return render(request, "admin/dashboard.html", payload)


def Clientdelete(request, pk):
    print("pk delete",pk)
    client.objects.get(pk=pk).delete()
    messages.info(request, 'client data deleted.')
    return redirect("dashboard")

def Clientupdate(request, pk):
    print("pk update",pk)
    
    if request.method == "POST":
        
        id_data = request.POST.get("id")
        update_data = client.objects.get(pk=id_data)


        update_data.first_name = request.POST.get("fname")
        update_data.last_name = request.POST.get("lname")
        update_data.address = request.POST.get("address")
        update_data.phone = request.POST.get("phone")
        update_data.email = request.POST.get("email")
        update_data.password = request.POST.get("password")

        try:
            update_data.coverpic = request.FILES["coverpic"]
        except:
            pass
        
        
        # new_data = client(cover_pic=coverpic,first_name=fname,last_name=lname,address=address,phone=phone,email=email,password=password)
        update_data.save()
        messages.info(request, 'client data updated.')
    return redirect("dashboard")


def DevicesList(request):
    if "id" not in request.session and "type" not in request.session and "email" not in request.session:
        return redirect("userlogin")

    admin_data = admins.objects.get(pk=request.session["id"])
    total_client = client.objects.all().count()
    total_devices = devices.objects.all().count()
    total_sharedevices = sharedevices.objects.all().count()
    # client_data = client.objects.all()
    device_data = devices.objects.all()

    payload = {"admin_data": admin_data, "device_data": device_data, "total_client": total_client, "total_devices": total_devices, "total_sharedevices": total_sharedevices}

    return render(request, "admin/devices.html", payload)


def DevicesUpdate(request):
    if "id" not in request.session and "type" not in request.session and "email" not in request.session:
        return redirect("userlogin")

    try:
        admin_data = admins.objects.get(pk=request.session["id"])
        admin_data_dict={
            "id":admin_data.pk,"userEmail":admin_data.email,"userPass":admin_data.password,"userRegion":admin_data.region
        }
        print("admin_data_dict: ",admin_data_dict)
        # sonoff = Sonoff(username=admin_data.email,password=admin_data.password, region=admin_data.region)
        sonoff_devices_data = sonoff_opr.getDevices(admin_data_dict)
        print(sonoff_devices_data["devices"],"----------------")
        for i in sonoff_devices_data["devices"]:
            if devices.objects.filter(admin_id=admin_data,device_id=i["deviceid"]).exists() == False:
                devices(admin_id=admin_data,device_id=i["deviceid"],name=i["name"],device_status=i["status"]).save()
            else:
                update_data = devices.objects.filter(admin_id=admin_data,device_id=i["deviceid"])[0]
                update_data.admin_id=admin_data
                update_data.device_id=i["deviceid"]
                update_data.name=i["name"]
                update_data.device_status=i["status"]
                update_data.save()
            messages.info(request, 'client data updated.')
        # data ={"status":status.HTTP_201_CREATED,"sonoff_devices_data":sonoff_devices_data,}
        
    except Exception as e:
        data={"status":str(e)}
    finally:
        messages.info(request, 'devices up to date.')
        return redirect("deviceslist")

def ShareDevicesList(request):
    if "id" not in request.session and "type" not in request.session and "email" not in request.session:
        return redirect("userlogin")

    admin_data = admins.objects.get(pk=request.session["id"])
    total_client = client.objects.all().count()
    total_devices = devices.objects.all().count()
    total_sharedevices = sharedevices.objects.all().count()
    # client_data = client.objects.all()
    sharedevices_data = sharedevices.objects.all()

    payload = {"admin_data": admin_data, "sharedevices_data": sharedevices_data, "total_client": total_client, "total_devices": total_devices, "total_sharedevices": total_sharedevices}

    return render(request, "admin/sharedeviceslist.html", payload)


def ShareDevicesdelete(request,pk):
    sharedevices.objects.get(pk=pk).delete()
    messages.info(request, 'shared devices deleted.')
    return redirect("sharedeviceslist") 

def ShareDevices(request, pk):
    if "id" not in request.session and "type" not in request.session and "email" not in request.session:
        return redirect("userlogin")
    admin_data = admins.objects.get(pk=request.session["id"])
    total_client = client.objects.all().count()
    total_devices = devices.objects.all().count()
    total_sharedevices = sharedevices.objects.all().count()
    client_data = client.objects.all()
    devices_data = devices.objects.all()
    sharedevices_data = sharedevices.objects.all()
    payload = {"client_data": client_data, "devices_data": devices_data, "admin_data": admin_data, "sharedevices_data": sharedevices_data, "total_client": total_client, "total_devices": total_devices, "total_sharedevices": total_sharedevices}

    if pk == 0:
        if request.method == "POST":
            client_id = request.POST.get("client_id")
            device_pk = request.POST.get("device_pk")
            from_date = request.POST.get("from_date")
            to_date = request.POST.get("to_date")
            status = request.POST.get("status")
            print(client_id, device_pk, from_date, to_date, status)
            client_id = client.objects.get(pk=int(client_id))
            device_pk = devices.objects.get(pk=int(device_pk))
            sharedevices_date = sharedevices(client_id=client_id, device_pk=device_pk, from_date=from_date, to_date=to_date, sharedevices_status=status)

            sharedevices_date.save()
            messages.success(request, 'devices shared successfully.')
            return redirect("sharedevices", 0)
    else:
        sharedevices_update = sharedevices.objects.get(pk=pk)
        payload["sharedevices_update"] = sharedevices_update
        if request.method == "POST" and "update" in request.POST:
            client_id = request.POST.get("client_id")
            device_pk = request.POST.get("device_pk")
            client_id = client.objects.get(pk=int(client_id))
            device_pk = devices.objects.get(pk=int(device_pk))
            sharedevices_update.client_id = client_id
            sharedevices_update.device_pk = device_pk
            sharedevices_update.from_date = request.POST.get("from_date")
            sharedevices_update.to_date = request.POST.get("to_date")
            sharedevices_update.sharedevices_status = request.POST.get("status")
            sharedevices_update.save()
            messages.info(request, 'shared devices updated.')
            return redirect("sharedeviceslist")
        return render(request, "admin/sharedevices.html", payload)
    return render(request, "admin/sharedevices.html", payload)