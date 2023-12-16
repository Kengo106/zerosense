from django.contrib import admin
from .api.models import Game, GameRule, Vote, Race, Horse, HorsePlace, GameComment, User, GamePlayer

admin.site.register(Game)
admin.site.register(GameRule)
admin.site.register(Vote)
admin.site.register(Race)
admin.site.register(Horse)
admin.site.register(HorsePlace)
admin.site.register(GameComment)
admin.site.register(User)
admin.site.register(GamePlayer)
