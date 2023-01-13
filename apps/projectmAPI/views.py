import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from .queries import *
from .shapers import *
from .validators import *



class UsersListView(ListAPIView):
    queryset = UserM.objects.all()
    serializer_class = UsersSerializer

class IsUserExistsView(APIView):

    def post(self, request):
        try:
            query = UserM.objects.get(pk=request.data['uid'])
        except:
            try:
                query = UserM.objects.get(nickname=request.data['nickname'])
            except:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsersSerializer(query)
        output_data = serializer.data
        return Response(output_data)


class UserInfoView(APIView):

    def get(self, request, uid):
        query = UserM.objects.get(pk=uid)
        serializer = UsersSerializer(query)
        output_data = serializer.data
        return Response(output_data)


class UserSelfInfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        query = request.user
        serializer = UsersSerializer(query)
        output_data = serializer.data
        return Response(output_data)


class UserClubsView(ListAPIView):

    serializer_class = UserClubsListSerializer
    
    def get_queryset(self):
        uid = self.kwargs['uid']
        if not hasattr(self, 'roles'):
            self.roles = ['Member', 'Judge', 'Vice-President', 'President']
        print(self.roles)
        queryset =  ClubUser.objects.all().filter(userm=uid, role_in_club__in=self.roles)
        return queryset
    
    def post(self, request, *args, **kwargs):
        #try:
        if 'role_in_club' in request.data:
            self.roles = [request.data['role_in_club'],]
            return self.list(request, *args, **kwargs)
        elif 'roles_in_club' in request.data:
            self.roles = request.data['roles_in_club'] 
            if isinstance(self.roles, str):
                self.roles = json.loads(self.roles)
            if isinstance(self.roles, list):
                return self.list(request, *args, **kwargs)
            return Response({'error': 'roles_in_club must be an array'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'role_in_club field required'}, status=status.HTTP_400_BAD_REQUEST)
        #except:
        #    return Response({'error': 'check request'}, status=status.HTTP_400_BAD_REQUEST)



class UserInClubStatView(APIView):
    
    def get(self, request, uid, cid):
        
        query = UserInClybStatQuery(uid, cid).query
        serializer = UserInClubRoleStatSerializer(query)
        output_data = UserInClubStatShaper(serializer.data).data
        return Response(output_data)

    def post(self, request, uid, cid):
        query = UserInClybStatQuery(uid, cid,
                                    request.data['date_start'], 
                                    request.data['date_end']).query
        serializer = UserInClubRoleStatSerializer(query)
        output_data = UserInClubStatShaper(serializer.data).data
        return Response(output_data)


class UserClubGamesView(APIView):

    def get(self, request, uid, cid):
        query = Game.objects.all().filter(
            game_userm_mtm__userm_id=uid,
            club_id=cid,
            game_userm_mtm__role__in=GAME_ROLES[:4]
        )
        serializer = GamesSerializer(query, many=True)
        output_data = serializer.data
        return Response(output_data)


class ClubsListView(ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubsSerializer


class ClubAddView(APIView):
    permission_classes = [IsAuthenticated]
    from rest_framework.request import Request
    
    def post(self, request: Request):
        club_data = request.data
        if not ClubAddValidation(club_data).is_valid:
            return Response({'error': 'Check your fields'}, status=status.HTTP_400_BAD_REQUEST)
        query = ClubAddQuey(request).query
        output_data = ClubsSerializer(query).data
        return Response(output_data)


class AddUserToClubView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ClubUser.objects.all()
    serializer_class = AddUserToClubSerializer


class ClubInfoView(APIView):

    def get(self, request, cid):

        query = Club.objects.get(pk=cid)
        serializer = ClubsSerializer(query)
        output_data = serializer.data
        return Response(output_data)


class ClubUsersListView(ListAPIView):
    serializer_class = ClubUsersListSerializer
    def get_queryset(self):
        cid = self.kwargs['cid']
        queryset = ClubUsersListQuery(cid).query
        return queryset


class ClubUsersScoreboardListView(ListAPIView):
    serializer_class = ClubUsersScoreboardListSerializer
    def get_queryset(self):
        cid = self.kwargs['cid']
        queryset = GameUser.objects.all().filter(game__club=cid)\
            .values('userm_id', 'userm__nickname')\
            .annotate(points_total=Coalesce(Sum('points'), 0.0))
        return queryset
    


class ClubGamesView(ListAPIView):
    serializer_class = GamesSerializer

    def get_queryset(self):
        cid = self.kwargs['cid']
        queryset = Game.objects.all().filter(club=cid)
        return queryset


class GamesListView(ListAPIView):
    serializer_class = GamesSerializer
    queryset = Game.objects.all()


class GameStatView(APIView):

    def get(self, request, gid):
        query = GameStatQuery(gid).query
        serializer = GameStatSerializer(query, many=True)
        output_data = GameStatShaper(serializer.data).data
        print(output_data)
        return Response(output_data)

class GameAddView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        game_description = request.data
        value = GameAddValidator(game_description.copy()).is_valid
        

        if not value:
            return Response('Ошибка формы, проверьте поля и checksum', status=status.HTTP_400_BAD_REQUEST)
        query = GameAddQuery(game_description).query
        print(query)
        return Response({'post': 'success'})




#Может быть полезно
#class ClubGamesView(GenericAPIView):
#
#    serializer_class = ClubGamesSerializer
#    
#    def list(self, request, *args, **kwargs):
#        queryset = self.filter_queryset(self.get_queryset())
#        page = self.paginate_queryset(queryset)
#        if page is not None:
#            serializer = self.get_serializer(page, many=True)
#            serializer = self.split_t(serializer)
#            return self.get_paginated_response(serializer.data)
#        serializer = self.get_serializer(queryset, many=True)
#        serializer = self.split_t(serializer)
#        return Response(serializer.data)
#
#
#    def split_t(self, serializer):
#        for i, field in enumerate(serializer.data):
#                for l, user in enumerate(field['players']):
#                    splited = serializer.data[i]['players'][l].split('|slice|1vmfq1|')
#                    serializer.data[i]['players'][l] = {'id': int(splited[0]),
#                        'nickname': splited[1],
#                        'role': splited[2]
#                    }
#        return serializer
#
#
#    def get_queryset(self):
#        cid = self.kwargs['cid']
#        queryset = ClubGamesQuery(cid).query
#        return queryset
#
#
#    def get(self, request, *args, **kwargs):
#        return self.list(request, *args, **kwargs)