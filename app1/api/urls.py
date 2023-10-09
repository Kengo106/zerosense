from django.urls import path
from app1.api.views import ApiRaceView, ApiUIDView, ApiNewGameView, ApiGameView,  ApiVoteView, APIScoreView, APIUserNameView, APIRaceResultView, APIAccountView, APISarchGameView
urlpatterns = [
    path('race/', ApiRaceView.as_view(), name='api-race'),
    path('UID/', ApiUIDView.as_view(), name='api-uid'),
    path('newgame/', ApiNewGameView.as_view(), name='api-newgame'),
    path('game/', ApiGameView.as_view(), name='api-game'),
    path('vote/', ApiVoteView.as_view(), name='api-vote'),
    path('score/', APIScoreView.as_view(), name='api-score'),
    path('username/', APIUserNameView.as_view(), name='api-username'),
    path('raceresult/', APIRaceResultView.as_view(), name='api-raceresult'),
    path('account/', APIAccountView.as_view(), name='api-account'),
    path('serchgame/', APISarchGameView.as_view(), name='api-serchgame')
]
