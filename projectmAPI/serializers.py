from rest_framework import serializers


class UserMSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=40)
    city = serializers.CharField(max_length=40)
    photo = serializers.CharField()
    socail = serializers.ListField()
