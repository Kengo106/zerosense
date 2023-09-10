from django.core.exceptions import ValidationError
from django.db import models
from datetime import date


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
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    horse_first = models.ForeignKey(
        Horse, on_delete=models.CASCADE, related_name='votes_first')
    horse_second = models.ForeignKey(
        Horse, on_delete=models.CASCADE, related_name='votes_second')
    horse_third = models.ForeignKey(
        Horse, on_delete=models.CASCADE, related_name='votes_third')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True)


class Odds(models.Model):
    Race = models.ForeignKey(Race, on_delete=models.CASCADE)
    tan = models.IntegerField(default=0)
    fuku_1 = models.IntegerField(default=0)
    fuku_2 = models.IntegerField(default=0)
    fuku_3 = models.IntegerField(default=0)
    umaren = models.IntegerField(default=0)
    umatan = models.IntegerField(default=0)
    wide_12 = models.IntegerField(default=0)
    wide_13 = models.IntegerField(default=0)
    wide_23 = models.IntegerField(default=0)
    renfuku_3 = models.IntegerField(default=0)
    rentan_3 = models.IntegerField(default=0)
