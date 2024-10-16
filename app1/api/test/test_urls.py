from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import ApiGameslistView, ApiGamesPlayerDeleteView, ApiGamesPlayerRegistView, ApiNewGameView, APIRaceResultView, ApiRaceView, APISarchGameView, APIScoreView, APIUserEditView, APIUserRegistView, APIView, ApiVoteView


class TestUrls(SimpleTestCase):

    def test_race_result_url(self):
        view = resolve('/api/races/test/games/test/')
        self.assertEqual(view.func.view_class, APIRaceResultView)

    def test_race_url(self):
        view = resolve('/api/races/')
        self.assertEqual(view.func.view_class, ApiRaceView)

    def test_games_player_delete_url(self):
        view = resolve('/api/player/delete/test/test/')
        self.assertEqual(view.func.view_class, ApiGamesPlayerDeleteView)

    def test_games_player_regist_url(self):
        view = resolve('/api/player/regist/test/')
        self.assertEqual(view.func.view_class, ApiGamesPlayerRegistView)

    def test_serch_game_url(self):
        view = resolve('/api/games/serch/')
        self.assertEqual(view.func.view_class, APISarchGameView)

    def test_score_url(self):
        view = resolve('/api/games/scores/test/')
        self.assertEqual(view.func.view_class, APIScoreView)

    def test_games_list_url(self):
        view = resolve('/api/games/list/test/')
        self.assertEqual(view.func.view_class, ApiGameslistView)

    def test_new_game_url(self):
        view = resolve('/api/games/create/')
        self.assertEqual(view.func.view_class, ApiNewGameView)

    def test_vote_url(self):
        view = resolve('/api/votes/')
        self.assertEqual(view.func.view_class, ApiVoteView)

    def test_user_regist_url(self):
        view = resolve('/api/user/regist/')
        self.assertEqual(view.func.view_class, APIUserRegistView)

    def test_user_edit_url(self):
        view = resolve('/api/user/edit/test/')
        self.assertEqual(view.func.view_class, APIUserEditView)
