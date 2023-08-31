from django.urls import path
from app1.api.views import ApiRaceView, ApiOddsView, ApiRaceNameView, ApiResultOddsview, ApiJoinView, ApiUIDView, ApiNewGameView, ApiJoinGameView, ApiRaceView, ApiVoteView

urlpatterns = [
    path('race/', ApiRaceView.as_view(), name='api-race'),
    path('odds/', ApiOddsView.as_view(), name='api-odds'),
    path('racename/', ApiRaceNameView.as_view(), name='api-racename'),
    path('resultodds/', ApiResultOddsview.as_view(), name='api-resultodds'),
    path('join/', ApiJoinView.as_view(), name='api-join'),
    path('UID/', ApiUIDView.as_view(), name='api-uid'),
    path('newgame/', ApiNewGameView.as_view(), name='api-newgame'),
    path('joingame/', ApiJoinGameView.as_view(), name='api-newgame'),
    path('vote/', ApiVoteView.as_view(), name='api-vote'),
]
