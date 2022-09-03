from datetime import datetime, date
from .models import *
from django.db.models import Count, Q, Avg, Sum, When, Case, Value
from django.db.models.lookups import LessThanOrEqual
from django.db.models.functions import Coalesce, Concat
from django.contrib.postgres.aggregates import ArrayAgg
from .global_fields import *


class UserInClybStatQuery:

    def __init__(self, uid, cid, date_start=date(2000, 1, 1), date_end=date.today()):
        
        aggregate_kwargs = {}
        for i, role in enumerate(GAME_ROLES[:4]):
            postfix = role[:3].lower()
            aggregate_kwargs.update({
                f'game_count_{postfix}': Count('game', filter=Q(role=role)),
                f'win_game_count_{postfix}': Count('game', filter=Q(game__result=GAME_RESULTS[i // 2]) & Q(role=role)),
                f'points_sum_{postfix}': Coalesce(Sum('points', filter=Q(role=role)), 0.0),
                f'points_avg_{postfix}': Coalesce(Avg('points', filter=Q(role=role)), 0.0),
                f'winrate_{postfix}':Case(
                    When(
                        LessThanOrEqual(Count('game', filter=Q(role=role)), 0),
                        then=0
                        ),
                    default=Count('game', filter=Q(game__result=GAME_RESULTS[i // 2]) & Q(role=role)) * 100 /
                    Count('game', filter=Q(role=role))
                )
            })
        aggregate_kwargs.update(
            {
                'game_count_tot': Count('game', filter=Q(role__in=GAME_ROLES[:4])),
                'win_game_count_tot': (
                    Count('game', filter=(Q(role='Mafia')|Q(role='Don'))&Q(game__result='Mafia'))+
                    Count('game', filter=(Q(role='Civilian')|Q(role='Commissioner'))&Q(game__result='City'))
                ),
                'points_sum_tot': Coalesce(Sum('points'), 0.0),
                'points_avg_tot': Coalesce(Avg('points'), 0.0),
                'winrate_tot':Case(
                    When(
                        LessThanOrEqual(Count('game'), 0),
                        then=0
                        ),
                    default=(
                    Count('game', filter=(Q(role='Mafia')|Q(role='Don'))&Q(game__result='Mafia'))+
                    Count('game', filter=(Q(role='Civilian')|Q(role='Commissioner'))&Q(game__result='City'))
                    ) * 100 /
                    Count('game')
                )
            }
        )
        self.query = GameUser.objects.all().filter(userm=uid,
            game__club=cid, 
            game__timestamp_start__gte=date_start, 
            game__timestamp_end__lte=date_end)\
            .aggregate(**aggregate_kwargs)


class ClubUsersListQuery:
    def __init__(self, cid):
        self.query = GameUser.objects.all().filter(game__club=cid)\
            .values('userm_id', 'userm__nickname')\
            .annotate(points_total=Coalesce(Sum('points'), 0.0))

                    
class GameStatQuery:

    def __init__(self, gid) -> None:
        self.query = GameUser.objects.all()\
            .filter(game_id=gid)\
            .values(
                'game', 'game__result',
                'game_id', 'game__timestamp_start',
                'game__timestamp_end',
                'game__days_description',
                'game__best_move',
                'game__judge_comments'
            )\
            .annotate(
                players=ArrayAgg('userm__nickname'), 
                ids=ArrayAgg('userm_id'), 
                roles=ArrayAgg('role')
            )

class GameAddQuery:

    def __init__(self, game_description) -> None:
        self.query = Game.objects.create(
            club=Club.objects.get(pk=game_description['club']['id']),
            timestamp_start=game_description['timestamp_start'],
            timestamp_end=game_description['timestamp_end'],
            days_description=game_description['days'],
            best_move=game_description['best_move'],
            result=game_description['result'],
            judge_comments=game_description['judge_comments'],
            checksum=game_description['checksum']
        )
        users = [
            GameUser(
                game=self.query,
                userm=UserM.objects.get(pk=game_description['players'][i]['id']),
                role=game_description['players'][i]['role'],
                fouls=game_description['players'][i]['fouls'],
                is_delete_from_game=game_description['players'][i]['is_delete'],
                delete_reason=game_description['players'][i]['delete_reason'],
                points=game_description['players'][i]['points'],
                points_description=game_description['players'][i]['points_description']
                ) for i in range(10)
            ]
        users += [
            GameUser(
                game=self.query,
                userm=UserM.objects.get(pk=game_description['judge']['id']),
                role='Judge',
                fouls=0,
                is_delete_from_game=False,
                delete_reason='Судья',
                points=0,
                points_description='Судья'
            )
        ]

        self.query = GameUser.objects.bulk_create(users)

        


#Может быть полезно
#class ClubGamesQuery:
#    def __init__(self, cid):
#        self.query = GameUser.objects.all()\
#            .filter(game__club=cid).values(
#                'game', 'game__timestamp_start', 
#                'game__timestamp_end', 'game__days_description',
#                'game__best_move', 'game__result',
#                'game__judge_comments'
#            )\
#            .annotate(
#                players=ArrayAgg(
#                    Concat(
#                        'userm_id',
#                        Value('|slice|1vmfq1|'),
#                        'userm__nickname', 
#                        Value('|slice|1vmfq1|'),
#                        'role',
#                        output_field=models.CharField()
#                    )
#                )
#            )
    
