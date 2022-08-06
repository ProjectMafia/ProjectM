from django.contrib import admin

from .models import *

admin.site.register(UserM)
admin.site.register(UserNicknameHistory)
admin.site.register(UserContact)
admin.site.register(Club)
admin.site.register(ClubContact)
admin.site.register(ServiceInfo)
admin.site.register(Game)
admin.site.register(ClubUser)
admin.site.register(GameUser)
