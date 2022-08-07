from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    contact = models.CharField('Контакт', max_length=50, default='номер')

    def __str__(self) -> str:
        return f'{self.contact}'

    class Meta:
        abstract = True


class ServiceInfo(models.Model):
    """Таблица для сервисов для таблицы контактов"""
    SERVICE_NAMES = (
        ('tg', 'Telegram'),
        ('vk', 'Вконтакте'),
        ('em', 'Email'),
        ('ph', 'Телефон'),
    )
    SERVICE_TYPES = (
        ('ph', 'Телефон'),
        ('em', 'Email'),
        ('et', 'Другое')
    )
    name = models.CharField('Название сервиса', max_length=2, choices=SERVICE_NAMES)
    logo = models.TextField('Ссылка на лого')
    type = models.CharField('Тип сервиса', max_length=2, choices=SERVICE_TYPES)

    def __str__(self) -> str:
        return f'{self.name}'
    

    class Meta:
        verbose_name = 'Доступный сервис'
        verbose_name_plural = 'Доступные сервисы'


class UserM(models.Model):
    "Таблица с пользователями, доделать аунтификацию"""""""
    login = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, default=-1)
    nickname = models.CharField('Ник', max_length=50, unique=True)
    email = models.CharField('Почта', max_length=50, unique=True)
    name = models.CharField('Имя', max_length=30)
    surname = models.CharField('Фамилия', max_length=30)
    country = models.CharField('Страна', max_length=40)
    city = models.CharField('Город', max_length=40)
    photo = models.URLField('Ссылка на фото профиля')
    scince_on_site = models.DateTimeField('На сайте с', auto_now=True)

    def __str__(self) -> str:
        return f'{self.nickname}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserNicknameHistory(models.Model):
    """История никнеймов"""
    uid = models.ForeignKey(UserM, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user_nickname_history')
    old_nickname = models.CharField('Старый никнейм', max_length=50)

    def __str__(self) -> str:
        return f'Старый ник пользователя: {self.old_nickname}'
    
    class Meta:
        verbose_name = 'Старый ник'
        verbose_name_plural = 'Старые ники'


class UserContact(Contact):
    """Контакты пользователя"""
    uid = models.ForeignKey(UserM, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user_contact')
    service_info = models.ForeignKey(ServiceInfo, on_delete=models.CASCADE, verbose_name='Информация о сервисе', 
    related_name='service_user_info')

    class Meta:
        verbose_name = 'Контакт игрока'
        verbose_name_plural = 'Контакты игрока'


class Club(models.Model):
    """Таблица клубов"""
    title = models.CharField('Название клуба', max_length=60, unique=True)
    country = models.CharField('Страна', max_length=40)
    city = models.CharField('Город', max_length=40)
    address = models.TextField('Адрес')
    desciption = models.TextField('Описание', default='Немногословный пчел')
    photo = models.TextField('Ссылка на фото профиля')
    scince_on_site = models.DateTimeField('На сайте с', auto_now=True)
    
    def __str__(self) -> str:
        return f'Клуб - {self.name}'

    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'


class ClubContact(Contact):
    """Контакты клуба"""
    cid = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name='Клуб', related_name='club_contact')
    service_info = models.ForeignKey(ServiceInfo, on_delete=models.CASCADE, verbose_name='Информация о сервисе', related_name='service_club_info')

    class Meta:
        verbose_name = 'Контакт клуба'
        verbose_name_plural = 'Контакты клуба'


class Game(models.Model):
    cid = models.ForeignKey(Club, on_delete=models.SET_NULL, verbose_name='Клуб игры',related_name='club_game', null=True)
    time_start = models.DateTimeField('Игра началась в ')
    time_end = models.DateTimeField('Игра закончилась в ')
    days = models.JSONField('Описание дней')
    best_move = models.JSONField('Лучший ход')
    result = models.BooleanField('True - победа мирных, False - мафия')
    comment = models.TextField('Комментарии судьи')
    checksum = models.TextField('Контрольная сумма')
    
    def __str__(self) -> str:
        return f'Игра {self.cid}. Победа {"мирныx" if self.result else "мафии"}'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'



class ClubUser(models.Model):
    uid = models.ForeignKey(UserM, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user_club_mtm')
    cid = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name='Клуб', related_name='club_user_mtm')
    ROLES = (
        ('G', 'Игрок'),
        ('J', 'Судья'),
        ('P', 'Президент'),
        ('S', 'Зам президента'),
    )
    role = models.CharField('Роль в клубе', max_length=1, choices=ROLES)

    def __str__(self) -> str:
        return f'Игрок {self.uid}, роль в клубе - {self.role}'

    class Meta:
        verbose_name = 'Связь клуба и пользователя'
        verbose_name_plural = 'Связь клубов и пользователей'


class GameUser(models.Model):
    ROLES = (
        ('P', 'Мирный житель'),
        ('K', 'Комиссар'),
        ('M', 'Мафия'),
        ('D', 'Дон'),
        ('J', 'Судья')
    )
    gid = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игра', related_name='game_user_mtm')
    uid = models.ForeignKey(UserM, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user_game_mtm')
    role = models.CharField('Роль в игре', max_length=1, choices=ROLES)
    fouls = models.IntegerField('Количество фолов')
    is_delete = models.BooleanField('Удален ли игрок из игры')
    delete_reason = models.TextField('Причина удаления')
    points = models.FloatField('Итоговые очки за игру')
    points_reason = models.TextField('За что даны очки')

    def __str__(self) -> str:
        return f'Игра - {self.gid}, пользователь - {self.uid}, роль - {self.role}'

    class Meta:
        verbose_name = 'Связь игры и пользователя'
        verbose_name_plural = 'Свяхи игр и пользователей'
