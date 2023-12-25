from django.urls import path
from .views import ApiRaceView,  ApiNewGameView, ApiGameslistView,  ApiVoteView, APIScoreView, APIUserEditView, APIRaceResultView,  APISarchGameView, APIUserRegistView, ApiGamesPlayerRegistView, ApiGamesPlayerDeleteView
# urls.py

from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="zerosense backend API",
        default_version='v1',
        description="zerosenseのバックエンドのAPI仕様です",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# urlは最後スラッシュで終わる
urlpatterns = [
    path('races/<str:racename>/games/<str:gameid>/',
         APIRaceResultView.as_view(), name='api-raceresult'),
    path('races/', ApiRaceView.as_view(), name='api-race'),
    path('player/delete/<str:gameid>/<str:uid>/',
         ApiGamesPlayerDeleteView.as_view(), name='api-game'),
    path('player/regist/<str:gameid>/',
         ApiGamesPlayerRegistView.as_view(), name='api-game'),
    path('games/scores/<str:gameid>/', APIScoreView.as_view(), name='api-score'),
    path('games/serch/', APISarchGameView.as_view(), name='api-game'),
    path('games/list/<str:uid>/',
         ApiGameslistView.as_view(), name='api-game-data'),
    path('games/create/', ApiNewGameView.as_view(), name='api-newgame'),
    path('votes/', ApiVoteView.as_view(), name='api-vote'),
    path('user/regist/', APIUserRegistView.as_view(), name='api-user'),
    path('user/edit/<str:uid>/', APIUserEditView.as_view(), name='api-user'),



]

if settings.DEBUG:
    # drf-yasgのURL設定

    urlpatterns += [

        path('swagger/', schema_view.with_ui('swagger',
                                             cache_timeout=0), name='schema-swagger-ui'),

        path('redoc/', schema_view.with_ui('redoc',
                                           cache_timeout=0), name='schema-redoc'),
        # yamlファイルで出力
        path('swagger.yaml', schema_view.without_ui(
            cache_timeout=0), name='schema-swagger-yaml'),

    ]
