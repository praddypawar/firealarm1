"""
ASGI config for firealarm project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firealarm.settings')

# application = get_asgi_application()

"""
ASGI config for  project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
#from django.conf.urls import url
from django.urls import include, re_path
from channels.auth import AuthMiddlewareStack
from firealarm.consumer import FireAlarmConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
import firealarm.routing
# from Authenticate.user_consumer import UserConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firealarm.settings')

# application = get_asgi_application()
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # re_path(r'^firealarm/(?P<user_id>\w+)/(?P<role_id>\w+)/(?P<user_type>\w+)/$', FireAlarmConsumer.as_asgi()),
            re_path(r'^firealarm/(?P<user_id>\w+)/$', FireAlarmConsumer.as_asgi()),
        ])
    ),
})
app = application
