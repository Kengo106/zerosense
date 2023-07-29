from django.core.exceptions import ValidationError
from django.db import models


class RaceResult(models.Model):
    # result_datum["馬名"] = horse_str
    horse_name = models.CharField(max_length=255, null=True)
    horse_number = models.IntegerField(
        null=True)  # result_datum["馬番"] = num_num
    race_name = models.CharField(
        max_length=255, null=True)  # result_datum["レース名"]
    place_num = models.IntegerField(null=True)  # result_datum["着順"]
    jockey_name = models.CharField(
        max_length=255, null=True)  # result_datum["騎手名"]
    trainer_name = models.CharField(
        max_length=255, null=True)  # result_datum["調教師名"]
    # result_datum["タイム"](文字型になっている)
    time = models.CharField(max_length=255, null=True)
    h_weight = models.FloatField(null=True)  # result_datum["馬体重"]
    pop = models.IntegerField(null=True)  # pop_num
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.race_name + " " + self.horse_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["horse_name", "race_name"], name="unique_race_result")
        ]


class Odds(models.Model):
    # result_datum["馬名"] = horse_str
    horse_name = models.CharField(max_length=255, null=True)
    horse_number = models.IntegerField(null=True)
    race_name = models.CharField(
        max_length=255, null=True)  # result_datum["レース名"]
    odds_tan = models.FloatField(null=True)
    odds_fuku_min = models.FloatField(null=True)
    odds_fuku_max = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.race_name + " " + self.horse_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["horse_name", "race_name"], name="unique_odds")
        ]


class JoinResultOdds(models.Model):
    RaceResult = models.OneToOneField(RaceResult, on_delete=models.CASCADE)
    Odds = models.OneToOneField(Odds, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.RaceResult_id} - {self.Odds_id}"


class GameRule(models.Model):
    rule_start_datetime = models.DateTimeField()
    rule_end_datetime = models.DateTimeField()
    open = models.BooleanField()
    logic_id = models.IntegerField()


class Game(models.Model):
    GameRule = models.ForeignKey(GameRule, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    GameRace = models.ForeignKey("GameRace", on_delete=models.CASCADE,)
    start_datetime = models.DateTimeField()


class Vote(models.Model):
    UID = models.CharField()
    Game = models.ForeignKey(Game, on_delete=models.CASCADE)
    horse_id_first = models.IntegerField()
    horse_id_second = models.IntegerField()
    horse_id_third = models.IntegerField()
    vote_time = models.DateTimeField()
    comment = models.TextField()


class GameRace(models.Model):
    JoinResultOdds = models.ForeignKey(
        JoinResultOdds, on_delete=models.CASCADE, null=True)
    race_name = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)


class GameRaceHorse(models.Model):
    GameRace = models.ForeignKey(GameRace, on_delete=models.CASCADE, null=True)
    horse_name = models.CharField(max_length=255)


class Comment(models.Model):
    Game = models.ForeignKey(Game, on_delete=models.CASCADE)
    UID = models.CharField()
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
