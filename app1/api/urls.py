from django.urls import path
from app1.api.views import ApiRaceView, ApiOddsView, ApiRaceNameView, ApiResultOddsview, ApiJoinView, ApiUIDView, ApiNewGameView

urlpatterns = [
    path('race/', ApiRaceView.as_view(), name='api-race'),
    path('odds/', ApiOddsView.as_view(), name='api-odds'),
    path('racename/', ApiRaceNameView.as_view(), name='api-racename'),
    path('resultodds/', ApiResultOddsview.as_view(), name='api-resultodds'),
    path('join/', ApiJoinView.as_view(), name='api-join'),
    path('UID/', ApiUIDView.as_view(), name='api-uid'),
    path('newgame/', ApiNewGameView.as_view(), name='api-newgame'),
]
