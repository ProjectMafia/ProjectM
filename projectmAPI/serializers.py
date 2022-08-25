from rest_framework import serializers
from CustomUser.models import *

class test(serializers.ModelSerializer):

    class Meta:
        model = UserM
        fields = '__all__'