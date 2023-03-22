from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("admin/",views.AdminList.as_view()),
    path("admin/<int:pk>",views.AdminDetail.as_view()),

    path("client/",views.ClientList.as_view()),
    path("client/<int:pk>",views.ClientDetail.as_view()),

    path("devices/",views.DevicesList.as_view()),

    path("share-device/",views.SharedevicesList.as_view()),
    path("share-device/<int:pk>",views.SharedevicesDetail.as_view()),
    
    path("client-dashboard/",views.ClientDashboard.as_view()),
    path("client-login/",views.ClientLogin.as_view()),
]