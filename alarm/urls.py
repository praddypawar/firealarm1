from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    # path('',views.index,name="index"),
    path("userlogin/",views.userlogin,name="userlogin"),
    path("operation/",views.operation,name="operation"),
    
    path("",views.UserLogin,name="userlogin"),
    path("dashboard/",views.Dashboard,name="dashboard"),
    path("logout/",views.Logout,name="logout"),


    #Clientdelete
    path("client-delete-<int:pk>/",views.Clientdelete,name="clientdelete"),
    path("client-update-<int:pk>/",views.Clientupdate,name="clientupdate"),

    path("devices-list/",views.DevicesList,name="deviceslist"),
    path("devices-update/",views.DevicesUpdate,name="devicesupdate"),

    
    path("share-devices-list/",views.ShareDevicesList,name="sharedeviceslist"),
    path("share-devices-<int:pk>/",views.ShareDevices,name="sharedevices"),
    path("share-devices-delete<int:pk>/",views.ShareDevicesdelete,name="sharedevicesdelete"),

    
]
