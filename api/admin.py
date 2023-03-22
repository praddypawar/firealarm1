from django.contrib import admin
from .models import admins,client,devices,sharedevices
# Register your models here.

admin.site.register(admins)
admin.site.register(client)
admin.site.register(devices)
admin.site.register(sharedevices)



