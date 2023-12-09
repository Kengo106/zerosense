from django.urls import path
from app1.api.views import ApiRaceView, ApiUIDView, ApiNewGameView, ApiGameView,  ApiVoteView, APIScoreView, APIUserNameView, APIRaceResultView, APIAccountView, APISarchGameView
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
        contact=openapi.Contact(email="contact@sample.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# urls.py


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

if settings.DEBUG:
    # drf-yasgのURL設定

    urlpatterns += [
        # ...
        path('swagger/', schema_view.with_ui('swagger',
                                             cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc',
                                           cache_timeout=0), name='schema-redoc'),
        # ...
    ]
