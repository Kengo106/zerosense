from django.core.exceptions import ValidationError
from django.db import models
from datetime import date


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


class User(models.Model):
    UID = models.CharField(max_length=255)
    username = models.CharField(max_length=255)


class GameRule(models.Model):
    span = models.CharField(max_length=255)
    open = models.BooleanField()
    logic_id = models.IntegerField()


class Game(models.Model):
    GameRule = models.ForeignKey(GameRule, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    start_datetime = models.DateTimeField(auto_now_add=True)


class Race(models.Model):
    race_name = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    race_date = models.DateField(default=date.today)
    is_votable = models.IntegerField(default=0)


class GamePlayer(models.Model):
    Game = models.ForeignKey(Game, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)


class Horse(models.Model):
    Race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True)
    horse_name = models.CharField(max_length=255)


class HorsePlace(models.Model):
    Horse = models.ForeignKey(Horse, on_delete=models.CASCADE)
    place = models.IntegerField(null=True)


class GameComment(models.Model):
    Game = models.ForeignKey(Game, on_delete=models.CASCADE)
    UID = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class RaceComment(models.Model):
    Race = models.ForeignKey(Race, on_delete=models.CASCADE)
    UID = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    horse_first = models.ForeignKey(
        Horse, on_delete=models.CASCADE, related_name='votes_first')
    horse_second = models.ForeignKey(
        Horse, on_delete=models.CASCADE, related_name='votes_second')
    horse_third = models.ForeignKey(
        Horse, on_delete=models.CASCADE, related_name='votes_third')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
