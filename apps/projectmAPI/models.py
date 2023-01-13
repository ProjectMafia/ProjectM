from django.db import models

from .modelmixins import *
from apps.CustomUser.models import UserM

class Club(BaseStructModel, TimeStampMixin, 
           AddressMixin, DescriptionMixin):
    """Таблица клубов"""
    title = models.CharField('Название клуба', max_length=60, unique=True)
    
    def __str__(self) -> str:
        return f'{self.title}'

    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'


class Game(BaseStructModel, TimeStampMixin):
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, verbose_name='Принадлежность игры клубу', related_name='clubs_game', null=True)
    timestamp_start = models.DateTimeField('Игра началась в ', blank=True)
    timestamp_end = models.DateTimeField('Игра закончилась в ', blank=True)
    days_description = models.JSONField('Описание дней')
    best_move = models.JSONField('Лучший ход')
    TYPE_OF_RESULTS = (
        ('Mafia', 'Mafia'),
        ('City', 'City'),
        ('Draw', 'Draw')
    )
    result = models.CharField('Результат игры', max_length=5, choices=TYPE_OF_RESULTS)
    judge_comments = models.TextField('Комментарии судьи')
    checksum = models.TextField('Контрольная сумма')
    
    def __str__(self) -> str:
        return f'Игра клуба {self.club}. Победа {self.result}'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'



class ClubUser(BaseStructModel):
    userm = models.ForeignKey(UserM, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='userm_club_mtm')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name='Клуб', related_name='club_userm_mtm')
    CLUB_ROLES = (
        ('Member', 'Member'),
        ('Judge', 'Judge'),
        ('President', 'President'),
        ('Vice-President', 'Vice-President'),
    )
    role_in_club = models.CharField('Роль в клубе', max_length=14, choices=CLUB_ROLES)

    def __str__(self) -> str:
        return f'Игрок {self.userm}, роль в клубе - {self.role_in_club}'

    class Meta:
        unique_together = ('userm', 'club')
        verbose_name = 'Связь клуба и пользователя'
        verbose_name_plural = 'Связь клубов и пользователей'


class GameUser(BaseStructModel):
    IN_GAME_ROLES = (
        ('Civilian', 'Civilian'),
        ('Сommissioner', 'Сommissioner'),
        ('Mafia', 'Mafia'),
        ('Don', 'Don'),
        ('Judge', 'Judge')
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игра', related_name='game_userm_mtm')
    userm = models.ForeignKey(UserM, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='userm_game_mtm')
    role = models.CharField('Роль в игре', max_length=12, choices=IN_GAME_ROLES)
    fouls = models.IntegerField('Количество фолов')
    is_delete_from_game = models.BooleanField('Удален ли игрок из игры')
    delete_reason = models.TextField('Причина удаления', blank=True)
    points = models.FloatField('Итоговые очки за игру')
    points_description = models.TextField('За что даны очки')

    def __str__(self) -> str:
        return f'Game ID - {self.game_id}'

    class Meta:
        verbose_name = 'Связь игры и пользователя'
        verbose_name_plural = 'Свяхи игр и пользователей'
