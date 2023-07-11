from ..models import RaceResult, Odds, JoinResultOdds
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RaceResultSeriralizer, OddsSerilizer, RacenameSerializer, JoinResultOddsSerializer
from django.db.models import Subquery, OuterRef
from django_filters import rest_framework as filters


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
    
class FilterResult(filters.FilterSet):
    class Meta:
        model = RaceResult
        fields = '__all__'

class FilterOdds(filters.FilterSet):
    class Meta:
        model = Odds
        fields = '__all__'

class  FilterJoinResultOdds(filters.FilterSet):
    class Meta:
        model = JoinResultOdds
        fields= "__all__"
    
class ApiResultOddsview(APIView):
    def get(self, request, format=None):
        filterresult = FilterResult(request.query_params, queryset=RaceResult.objects.all())
        filterodds = FilterOdds(request.query_params, queryset=Odds.objects.all())
        result_serializer = RaceResultSeriralizer(instance=filterresult.qs, many=True)
        odds_serializer = OddsSerilizer(instance=filterodds.qs, many=True)
        return Response({
            "result": result_serializer.data,
            "odds": odds_serializer.data
        } )

class ApiJoinView(APIView):
    def get(self, request, format=None):
        filterjoin = FilterJoinResultOdds(
            request.query_params, queryset=JoinResultOdds.objects.select_related('RaceResult_id',"Odds_id").all())
        join_serializer = JoinResultOddsSerializer(instance=filterjoin.qs, many=True)
        return Response(join_serializer.data)
