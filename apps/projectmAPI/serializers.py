from unittest import result
from rest_framework import serializers
from apps.CustomUser.models import *
from apps.projectmAPI.models import *
from .global_fields import *
from django.contrib.postgres.fields import ArrayField


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserM
        fields = ('id', 'nickname', 'first_name', 'last_name', 'country', 'city', 'address', 'description')


class UserClubsListSerializer(serializers.Serializer):
    club_id = serializers.CharField()
    club_title = serializers.CharField(source='club')
    role_in_club = serializers.CharField()


class UserInClubRoleStatSerializer(serializers.Serializer):
    
    for role in GAME_ROLES:
        postfix = role[:3].lower()
        locals()[f'game_count_{postfix}'] = serializers.IntegerField()
        locals()[f'win_game_count_{postfix}'] = serializers.IntegerField()
        locals()[f'winrate_{postfix}'] = serializers.IntegerField()
        locals()[f'points_sum_{postfix}'] = serializers.DecimalField(max_digits=5, decimal_places=2)
        locals()[f'points_avg_{postfix}'] = serializers.DecimalField(max_digits=5, decimal_places=2)


class ClubsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = ('id', 'title', 'description', 'country', 'city', 'address')


class ClubUsersListSerializer(serializers.Serializer):
    userm_id = serializers.CharField()
    nickname = serializers.CharField(source='userm__nickname')


class ClubUsersScoreboardListSerializer(serializers.Serializer):
    userm_id = serializers.CharField()
    nickname = serializers.CharField(source='userm__nickname')
    points_total = serializers.FloatField()


class AddUserToClubSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClubUser
        fields = ('userm', 'club', 'role_in_club')


class GamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'result', 'timestamp_start', 'timestamp_end')
        

class GameStatSerializer(serializers.Serializer):
    
    game_id = serializers.IntegerField()
    timestamp_start = serializers.DateTimeField(source='game__timestamp_start')
    timestamp_end = serializers.DateTimeField(source='game__timestamp_end')
    days_description = serializers.JSONField(source='game__days_description')
    best_move = serializers.JSONField(source='game__best_move')
    result = serializers.CharField(source='game__result')
    judge_comments = serializers.CharField(source='game__judge_comments')
    ids = serializers.ListField()
    players = serializers.ListField()
    roles = serializers.ListField()

class GameAddSerializer(serializers.Serializer):

    def create(self, validated_data):
        
        return super().create(validated_data)





















#Может быть полезно
#class ClubGamesSerializer(serializers.Serializer):
#    game = serializers.IntegerField()
#    timestamp_start = serializers.DateTimeField(source='game__timestamp_start')
#    timestamp_end = serializers.DateTimeField(source='game__timestamp_end')
#    days_description = serializers.JSONField(source='game__days_description')
#    best_move = serializers.JSONField(source='game__best_move')
#    result = serializers.CharField(source='game__result')
#    judge_comments = serializers.CharField(source='game__judge_comments')
#    players = serializers.ListField()


    #class Meta:
    #    model = GameUser
    #    fields = ('id', 'days_description', 'best_move', 'result', 'judge_comments', 'users')
    







'''
class GameSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    days_description = serializers.JSONField()
    best_move = serializers.JSONField()
    result = serializers.CharField()
    judge_comments = serializers.CharField()
    timestamp_start = serializers.DateTimeField()
    timestamp_end = serializers.DateTimeField()


    


class UserInClubStatSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    class Meta:
        model = GameUser
        depth=1
        fields = ('id', 'role', 'fouls', 'is_delete_from_game', 'delete_reason', 'points', 'points_description', 'game')
        #fields = '__all__'
'''