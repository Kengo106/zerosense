from django.urls import path
from app1.api.views import ApiRaceView, ApiOddsView, ApiRaceNameView, ApiResultOddsview

urlpatterns = [
    path('race/', ApiRaceView.as_view(), name='api-race'),
    path('odds/', ApiOddsView.as_view(), name='api-odds'),
    path('racename/', ApiRaceNameView.as_view(), name='api-racename'),
    path('resultodds/', ApiResultOddsview.as_view(), name='api-resultodds') 
]
