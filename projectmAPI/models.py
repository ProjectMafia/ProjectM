from django.db import models

from .modelmixins import *
from CustomUser.models import UserM

class Club(BaseStructModel, TimeStampMixin, AddressMixin, DescriptionMixin):
    """Таблица клубов"""
    title = models.CharField('Название клуба', max_length=60, unique=True)
    club_login = models.CharField('Логин клуба', max_length=60, unique=True)
    
    def __str__(self) -> str:
        return f'Клуб - {self.title}'

    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'


class Game(BaseStructModel, TimeStampMixin):
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, verbose_name='Принадлежность игры клубу', related_name='clubs_game', null=True)
    timestamp_start = models.DateTimeField('Игра началась в ')
    timestamp_end = models.DateTimeField('Игра закончилась в ')
    days_description = models.JSONField('Описание дней')
    best_move = models.JSONField('Лучший ход')
    TYPE_OF_RESULTS = (
        ('M', 'Mafia'),
        ('C', 'City'),
        ('D', 'Draw')
    )
    result = models.CharField('Результат игры', max_length=1, choices=TYPE_OF_RESULTS)
    judge_comments = models.TextField('Комментарии судьи')
    checksum = models.TextField('Контрольная сумма')
    
    def __str__(self) -> str:
        return f'Игра клуба {self.club}. Победа {"мирныx" if self.result else "мафии"}'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'



class ClubUser(BaseStructModel):
    userm = models.ForeignKey(UserM, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='userm_club_mtm')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name='Клуб', related_name='club_userm_mtm')
    CLUB_ROLES = (
        ('G', 'Игрок'),
        ('J', 'Судья'),
        ('P', 'Президент'),
        ('S', 'Зам президента'),
    )
    role_in_club = models.CharField('Роль в клубе', max_length=1, choices=CLUB_ROLES)

    def __str__(self) -> str:
        return f'Игрок {self.userm}, роль в клубе - {self.role_in_club}'

    class Meta:
        verbose_name = 'Связь клуба и пользователя'
        verbose_name_plural = 'Связь клубов и пользователей'


class GameUser(BaseStructModel):
    IN_GAME_ROLES = (
        ('P', 'Мирный житель'),
        ('K', 'Комиссар'),
        ('M', 'Мафия'),
        ('D', 'Дон'),
        ('J', 'Судья')
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игра', related_name='game_userm_mtm')
    userm = models.ForeignKey(UserM, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='userm_game_mtm')
    role = models.CharField('Роль в игре', max_length=1, choices=IN_GAME_ROLES)
    fouls = models.IntegerField('Количество фолов')
    is_delete = models.BooleanField('Удален ли игрок из игры')
    delete_description = models.TextField('Причина удаления')
    points = models.FloatField('Итоговые очки за игру')
    points_description = models.TextField('За что даны очки')

    def __str__(self) -> str:
        return f'Игра - {self.game}, пользователь - {self.userm}, роль - {self.role}'

    class Meta:
        verbose_name = 'Связь игры и пользователя'
        verbose_name_plural = 'Свяхи игр и пользователей'
