from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from CustomUser import *
from .serializers import *
from rest_framework.response import Response


class CivilianStatsView(APIView):

    def get(self, request, uid, format=None):
        query = UserM.objects.all()
        
        return Response(test(query, many=True).data)


