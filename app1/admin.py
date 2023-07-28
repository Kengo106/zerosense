from django.contrib import admin
from .models import RaceResult, Odds, JoinResultOdds, Game, GameRule, Vote, GameResult, GameHorse, Comment

admin.site.register(RaceResult)
admin.site.register(Odds)
admin.site.register(JoinResultOdds)
admin.site.register(Game)
admin.site.register(GameRule)
admin.site.register(Vote)
admin.site.register(GameResult)
admin.site.register(GameHorse)
admin.site.register(Comment)
