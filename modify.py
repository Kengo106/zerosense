import django
django.setup()
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zerosence.settings")


from django.db import transaction
from app1.models import JoinResultOdds, Odds, RaceResult
from app1.api.serializers import OddsSerilizer, RaceResultSeriralizer
from app1.api.views import FilterOdds

def get_raceresult():
        race_results = RaceResult.objects.order_by("-created_at").exclude(
             id__in=JoinResultOdds.objects.values_list("RaceResult_id",flat=True)).all()
        serialized_data_list = []
        for race_result in race_results:
            Serializer_result = RaceResultSeriralizer(race_result)
            datamu = {}
            datamu["RaceResult_id"] = Serializer_result.data["id"]
            serializer_data = {
                "horse_name": Serializer_result.data["horse_name"],
                "race_name": Serializer_result.data["race_name"]
            }

            filterset = FilterOdds(data=serializer_data, queryset=Odds.objects.all())
            Serializer_odds = OddsSerilizer(instance=filterset.qs, many=True)
            datamu["odds_id"] = Serializer_odds.data[0]["id"]

            serialized_data_list.append(datamu)
        
        with transaction.atomic():
            for result_data in serialized_data_list:
                
                JoinResultOdds.objects.update_or_create(
                    RaceResult=RaceResult.objects.get(id=result_data['RaceResult_id']),
                    Odds=Odds.objects.get(id=result_data["odds_id"]),
                )
    

if __name__ == "__main__":
    get_raceresult()
