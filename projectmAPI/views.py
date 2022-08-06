from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response

class UserAPIView(APIView):
    def get(self, request, format=None):
        query = UserM.objects.all()
        json = UserMSerializer(query, many=True)
        return Response(json.data)

