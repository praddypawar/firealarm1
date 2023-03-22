from django.conf.urls import url

from firealarm.consumer import FireAlarmConsumer

websocket_urlpatterns = [
    url(r'^ws/', FireAlarmConsumer.as_asgi()),
]