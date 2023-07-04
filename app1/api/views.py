from ..models import RaceResult, Odds
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RaceResultSeriralizer, OddsSerilizer, RacenameSerializer
from django.db.models import Subquery, OuterRef


class ApiRaceView(APIView):

    def get(self,request, format=None):
        return Response({"response": "GET RESULT recently 10 records"})

    def post(self,request, format=None):
        race_results = RaceResult.objects.order_by("-created_at").all()[:10]
        serialized_data_list = []
        for race_result in race_results:
            Serializer = RaceResultSeriralizer(race_result)
            serialized_data_list.append(Serializer.data)
            
        return Response(serialized_data_list)
    
class ApiOddsView(APIView):

    def get(self,request, format=None):
        return Response({"response": "GET ODDS recently 10 records"})
    
    def post(self,request, format=None):
        odds_results = Odds.objects.order_by('-created_at').all()[:10]
        serialized_data_list = []
        for odds_result in odds_results:
            Serializer = OddsSerilizer(odds_result)
            serialized_data_list.append(Serializer.data)
            
        return Response(serialized_data_list)
    
class ApiRaceNameView(APIView):
    
    def get(self, request, format=None):
        distinct_race_ids = RaceResult.objects.order_by('race_name', '-created_at').distinct('race_name').values('id')
        race_names = RaceResult.objects.filter(id__in=Subquery(distinct_race_ids)).order_by('-created_at')  # 分からないので後でSQLの勉強をする
        serializer = RacenameSerializer(race_names, many=True)
        return Response(serializer.data)