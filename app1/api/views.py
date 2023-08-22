from ..models import RaceResult, Odds, JoinResultOdds, User, Game, GameRule, GamePlayer, GameComment
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RaceResultSeriralizer, OddsSerilizer, RacenameSerializer, JoinResultOddsSerializer
from django.db.models import Subquery, OuterRef
from django_filters import rest_framework as filters
from rest_framework import status


class ApiRaceView(APIView):

    def get(self, request, format=None):
        return Response({"response": "GET RESULT recently 10 records"})

    def post(self, request, format=None):
        race_results = RaceResult.objects.order_by("-created_at").all()[:10]
        serialized_data_list = []
        for race_result in race_results:
            Serializer = RaceResultSeriralizer(race_result)
            serialized_data_list.append(Serializer.data)

        return Response(serialized_data_list)


class ApiOddsView(APIView):

    def get(self, request, format=None):
        return Response({"response": "GET ODDS recently 10 records"})

    def post(self, request, format=None):
        odds_results = Odds.objects.order_by('-created_at').all()[:10]
        serialized_data_list = []
        for odds_result in odds_results:
            Serializer = OddsSerilizer(odds_result)
            serialized_data_list.append(Serializer.data)

        return Response(serialized_data_list)


class ApiRaceNameView(APIView):

    def get(self, request, format=None):
        distinct_race_ids = RaceResult.objects.order_by(
            'race_name', '-created_at').distinct('race_name').values('id')
        race_names = RaceResult.objects.filter(id__in=Subquery(
            distinct_race_ids)).order_by('-created_at')
        serializer = RacenameSerializer(race_names, many=True)
        return Response(serializer.data)


class FilterResult(filters.FilterSet):
    class Meta:
        model = RaceResult
        fields = '__all__'


class FilterOdds(filters.FilterSet):
    class Meta:
        model = Odds
        fields = '__all__'


class FilterJoinResultOdds(filters.FilterSet):
    class Meta:
        model = JoinResultOdds
        fields = "__all__"


class ApiResultOddsview(APIView):
    def get(self, request, format=None):
        filterresult = FilterResult(
            request.query_params, queryset=RaceResult.objects.all())
        filterodds = FilterOdds(request.query_params,
                                queryset=Odds.objects.all())
        result_serializer = RaceResultSeriralizer(
            instance=filterresult.qs, many=True)
        odds_serializer = OddsSerilizer(instance=filterodds.qs, many=True)
        return Response({
            "result": result_serializer.data,
            "odds": odds_serializer.data
        })


class ApiJoinView(APIView):
    def get(self, request, format=None):
        race_name = request.query_params.get("race_name")
        join_query = JoinResultOdds.objects.select_related(
            'RaceResult', "Odds").filter(RaceResult__race_name=race_name)
        join_serializer = JoinResultOddsSerializer(
            instance=join_query, many=True)
        return Response(join_serializer.data)


class ApiUIDView(APIView):
    def post(self, request, format=None):
        uid = request.data.get('uid')
        username = request.data.get('username')
        try:
            User.objects.create(
                UID=uid,
                username=username
            )
            response = Response(
                {"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        except:
            response = Response({"message": "miss"},
                                status=status.HTTP_400_BAD_REQUEST)

        return response


class ApiNewGameView(APIView):
    def post(self, request, format=None):
        gamename = request.data.get("gamename")
        uid = request.data.get("uid")
        public = request.data.get("open")
        span = request.data.get("span")
        try:
            game_rule = GameRule.objects.create(
                span=span,
                open=public,
                logic_id=999
            )

            game = Game.objects.create(
                GameRule=game_rule,
                name=gamename,
            )

            GamePlayer.objects.create(
                Game=game,
                User=User.objects.filter(UID=uid).first()
            )
            return Response("Sucsess", status=status.HTTP_201_CREATED)
        except:
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)
