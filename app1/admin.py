from django.contrib import admin
from .models import RaceResult, Odds, JoinResultOdds, Game, GameRule, Vote, GameRace, GameRaceHorse, Comment

admin.site.register(RaceResult)
admin.site.register(Odds)
admin.site.register(JoinResultOdds)
admin.site.register(Game)
admin.site.register(GameRule)
admin.site.register(Vote)
admin.site.register(GameRace)
admin.site.register(GameRaceHorse)
admin.site.register(Comment)
