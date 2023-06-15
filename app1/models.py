from django.db import models

class RaceResult(models.Model):
    horse_name = models.CharField(max_length=255) #  result_datum["馬名"] = horse_str
    horse_number = models.IntegerField() #   result_datum["馬番"] = num_num
    race_name = models.CharField(max_length=255) #   result_datum["レース名"]
    place_num = models.IntegerField() #  result_datum["着順"]
    jockey_name = models.CharField(max_length=255) #  result_datum["騎手名"]
    trainer_name = models.CharField(max_length=255) #  result_datum["調教師名"]
    time = models.CharField(max_length=255) #  result_datum["タイム"](文字型になっている)
    h_weight = models.FloatField() #  result_datum["馬体重"]
    pop = models.IntegerField() #  pop_num
    
    # 他のフィールド...

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["horse_number", "race_name"], name="unique_race_result")
        ]
        
class Odds(models.Model):
    horse_name = models.CharField(max_length=255) #  result_datum["馬名"] = horse_str
    horse_number = models.IntegerField()
    race_name = models.CharField(max_length=255) #   result_datum["レース名"]
    odds_tan = models.FloatField()
    odds_fuku_min = models.FloatField()
    odds_fuku_max = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["horse_number", "race_name"], name="unique_odds")
        ]


