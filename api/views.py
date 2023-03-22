from django.shortcuts import render


from .serializers import AdminSerializer,ClientSerializer,DeviceSerializer,SharedeviceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import admins,client,devices,sharedevices
from rest_framework import status

from rest_framework import parsers
from utils.api.request import MultipartJsonParser
from django.http import Http404

from alarm import sonoff_opr

# Create your views here.

class AdminList(APIView):
    parser_classes = (MultipartJsonParser, parsers.JSONParser)

    def get(self,request,format=None):
        admin_data = admins.objects.all()
        serializer = AdminSerializer(admin_data,many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AdminDetail(APIView):
    def get_object(self,pk):
        try:
            return admins.objects.get(pk=pk)
        except admins.DoesNotExist as e:
            raise Http404 from e
    
    def get(self, request, pk, format=None):
        admin_data = self.get_object(pk)
        serializer = AdminSerializer(admin_data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        admin_data = self.get_object(pk)
        serializer = AdminSerializer(admin_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        admin_data = self.get_object(pk)
        admin_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientList(APIView):
    parser_classes = (MultipartJsonParser, parsers.JSONParser)

    def get(self,request,format=None):
        admin_data = client.objects.all()
        serializer = ClientSerializer(admin_data,many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ClientDetail(APIView):
    def get_object(self,pk):
        try:
            return client.objects.get(pk=pk)
        except client.DoesNotExist as e:
            raise Http404 from e
    
    def get(self, request, pk, format=None):
        client_data = self.get_object(pk)
        serializer = ClientSerializer(client_data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        client_data = self.get_object(pk)
        serializer = ClientSerializer(client_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        client_data = self.get_object(pk)
        client_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DevicesList(APIView):
    parser_classes = (MultipartJsonParser, parsers.JSONParser)

    def get(self,request,format=None):
        device_data = devices.objects.all()
        serializer = DeviceSerializer(device_data,many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            admin_data = admins.objects.get(pk=request.data["admin_id"])
            admin_data_dict={
                "id":admin_data.pk,"userEmail":admin_data.email,"userPass":admin_data.password,"userRegion":admin_data.region
            }
            sonoff_devices_data = sonoff_opr.getDevices(admin_data_dict)
            sonoff_devices_data["devices"]
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
            data ={"status":status.HTTP_201_CREATED,"sonoff_devices_data":sonoff_devices_data,}
            
        except Exception as e:
            data={"status":str(e)}
        finally:
            return Response(data)


class SharedevicesList(APIView):
    parser_classes = (MultipartJsonParser, parsers.JSONParser)

    def get(self,request,format=None):
        share_device = sharedevices.objects.all()
        serializer = SharedeviceSerializer(share_device,many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SharedeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SharedevicesDetail(APIView):
    def get_object(self,pk):
        try:
            return sharedevices.objects.get(pk=pk)
        except sharedevices.DoesNotExist as e:
            raise Http404 from e
    
    def get(self, request, pk, format=None):
        share_device = self.get_object(pk)
        serializer = SharedeviceSerializer(share_device)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        share_device = self.get_object(pk)
        serializer = SharedeviceSerializer(share_device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        share_device = self.get_object(pk)
        share_device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientDashboard(APIView):
    parser_classes = (MultipartJsonParser, parsers.JSONParser)

    def get(self,request,format=None):
        share_device = sharedevices.objects.all()
        serializer = SharedeviceSerializer(share_device,many=True)
        return Response(serializer.data)

class ClientLogin(APIView):
    def post(self,request,format=None):
        email = request.data["email"]
        password = request.data["password"]
        data =[]
        try:
            if client_data := list(client.objects.filter(email=email, password=password).values()):
                devices_id = list(sharedevices.objects.filter(client_id=client_data[0].get("id",0)).values("device_pk").distinct())
                _devices_list=[]
                for device_id in devices_id:
                    if device_list := list(devices.objects.filter(id=device_id.get("device_pk",0)).values()):
                        if admin_data := list(admins.objects.filter(pk=device_list[0].get("admin_id_id",0)).values()):
                            device_list[0].update({"admin_detail":admin_data[0]})
                        _devices_list.append(device_list[0])
                data.append({"client_data":client_data[0],"devices_list":_devices_list})
                
        except Exception as e:
            data[{"error": str(e)}]
        finally:
            return Response(data)

    