from django.contrib import admin

from .models import *


admin.site.register(Club)
admin.site.register(Game)
admin.site.register(ClubUser)
admin.site.register(GameUser)
