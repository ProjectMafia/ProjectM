from rest_framework import serializers


class UserMSerializer(serializers.Serializer):
    #nickname = serializers.CharField(max_length=50)
    #country = serializers.CharField(max_length=40)
    #city = serializers.CharField(max_length=40)
    #photo = serializers.CharField()
    #user_contact = serializers.IntegerField()
    service_info = serializers.CharField()
