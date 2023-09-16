from django.urls import path
from app1.api.views import ApiRaceView, ApiUIDView, ApiNewGameView, ApiJoinGameView,  ApiVoteView, APIScoreView, APIUserNameView

urlpatterns = [
    path('race/', ApiRaceView.as_view(), name='api-race'),
    path('UID/', ApiUIDView.as_view(), name='api-uid'),
    path('newgame/', ApiNewGameView.as_view(), name='api-newgame'),
    path('joingame/', ApiJoinGameView.as_view(), name='api-newgame'),
    path('vote/', ApiVoteView.as_view(), name='api-vote'),
    path('score/', APIScoreView.as_view(), name='api-score'),
    path('username/', APIUserNameView.as_view(), name='api=username'),
]
