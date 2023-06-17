from django.core.exceptions import ValidationError
from django.db import models

class RaceResult(models.Model):
    horse_name = models.CharField(max_length=255, null=True)  #  result_datum["馬名"] = horse_str
    horse_number = models.IntegerField(null=True)  #   result_datum["馬番"] = num_num
    race_name = models.CharField(max_length=255, null=True)  #   result_datum["レース名"]
    place_num = models.IntegerField(null=True)  #  result_datum["着順"]
    jockey_name = models.CharField(max_length=255, null=True)  #  result_datum["騎手名"]
    trainer_name = models.CharField(max_length=255, null=True)  #  result_datum["調教師名"]
    time = models.CharField(max_length=255, null=True)  #  result_datum["タイム"](文字型になっている)
    h_weight = models.FloatField(null=True)  #  result_datum["馬体重"]
    pop = models.IntegerField(null=True)  #  pop_num
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["horse_name", "race_name"], name="unique_race_result")
        ]
        
class Odds(models.Model):
    horse_name = models.CharField(max_length=255, null=True)  #  result_datum["馬名"] = horse_str
    horse_number = models.IntegerField(null=True)
    race_name = models.CharField(max_length=255, null=True)  #   result_datum["レース名"]
    odds_tan = models.FloatField(null=True)
    odds_fuku_min = models.FloatField(null=True)
    odds_fuku_max = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["horse_name", "race_name"], name="unique_odds")
        ]


