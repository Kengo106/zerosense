from django.test import TestCase
from .models import User, Game, GameRule, Race, Horse, HorsePlace, Vote, Odds
from .views import game_score
from django.test import RequestFactory
from datetime import date, timedelta


class GameScoreTestCase(TestCase):
    def setUp(self):

        self.user1 = User.objects.create(uid="user123", username="testuser")
        self.user2 = User.objects.create(uid="user456", username="testuser")
        self.user3 = User.objects.create(uid="user789", username="testuser")

        self.game_rule = GameRule.objects.create(start=date.today(
        ), end=date.today() + timedelta(days=7), open=False, logic_id=1)
        self.game = Game.objects.create(
            game_rule=self.game_rule, name="Test Game")
        self.race = Race.objects.create(race_name="Test Race", rank="G1", race_date=date.today(
        ), start_time=date.today(), is_votable=0)
        self.horse = []
        self.horse_place = []
        for i in range(1, 11):
            horse = Horse.objects.create(
                race=self.race, horse_name=f"Test Horse{i}")
            self.horse.append(horse)
            self.horse_place.append(HorsePlace.objects.create(
                horse=horse, place=i))

        self.vote = Vote.objects.create(user=self.user, game=self.game, race=self.race,
                                        horse_first=self.horse, horse_second=self.horse, horse_third=self.horse)
        self.odds = Odds.objects.create(race=self.race, tan=100, fuku_1=50, fuku_2=30, fuku_3=20,
                                        umaren=200, umatan=300, wide_12=70, wide_13=60, wide_23=80, trio=150, tierce=400)

        self.factory = RequestFactory()

    def test_game_score_calculation(self):

        request = self.factory.get(
            '/fake-url', {'gameid': str(self.game.id_for_serch)})
        _, response_data = game_score(request)

        expected_score = 100
        actual_score = response_data[0]["testuser"]["Test Race"]
        self.assertEqual(actual_score, expected_score)
