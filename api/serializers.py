from rest_framework import serializers
from .models import admins,client,devices,sharedevices

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = admins
        fields=[
            "id","first_name","last_name","email","password","region"
]

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = client
        fields=[
                "id","cover_pic","first_name","last_name","address","phone","email","password"
                ]


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = devices
        fields=[
                "id","admin_id","name","device_id","device_status"
                ]

class SharedeviceSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['from_date'] > data['to_date']:
            raise serializers.ValidationError("End date should be greater than start date.")
        return data
        
    class Meta:
        model = sharedevices
        fields=[
                "id","client_id","device_pk","from_date","to_date","sharedevices_status"
                ]