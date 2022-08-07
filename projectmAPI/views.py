from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.db.models import JSONField
class UserAPIView(APIView):
    def get(self, request, format=None):
        query = UserM.objects.get(pk=1).user_contact.all().annotate(service_info=JSONField('service_info'))
        json = UserMSerializer(query, many=True)
        print(query)
        return Response(json.data)

