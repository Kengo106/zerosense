from .models import User, Game, GameRule, GamePlayer, GameComment, Race, Horse, Vote, Odds, HorsePlace
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Subquery, OuterRef
from django_filters import rest_framework as filters
from rest_framework import status
from django.db import transaction
import traceback
from datetime import timedelta
from django.db.models.functions import ExtractMonth
import uuid
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils import judge_hit, get_odds, is_latest_week_race, calc_hit_time, calc_monthly_socere, game_info


class APIUserView(APIView):

    def post(self, request, format=None):  # 修正済み
        uid = request.data.get('uid')
        username = request.data.get('username')
        try:
            User.objects.create(
                uid=uid,
                username=username
            )
            response = Response(
                {"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        except:
            response = Response({"message": "miss"},
                                status=status.HTTP_400_BAD_REQUEST)

        return response

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='新しいユーザー名')
            },
        ),
        responses={
            200: openapi.Response(description="更新しました"),
            400: openapi.Response(description="Error")
        }
    )
    def put(self, request, uid, format=None):  # 修正済み
        try:
            update_name = request.data.get('name')
            User.objects.filter(uid=uid).update(username=update_name)
            return Response({"message": f'変更しました： {update_name}'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uid', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='ユーザーID', required=True)
        ],
        responses={200: openapi.Response(
            description="Success"), 400: openapi.Response(description="Error")}
    )
    def delete(self, request, uid, format=None):  # 修正済み
        try:
            with transaction.atomic():
                user = User.objects.filter(uid=uid).first()
                GamePlayer.objects.filter(user=user).delete()
                GameComment.objects.filter(user=user).delete()
                Vote.objects.filter(user=user).delete()
                user.delete()
            return Response({"Success"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)


class ApiNewGameView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('gamename', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='ゲーム名', required=True),
            openapi.Parameter('uid', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='ユーザーID', required=True),
            openapi.Parameter('public', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_BOOLEAN, description='公開設定', required=True),
            openapi.Parameter('span', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_OBJECT, description='ゲーム期間', required=True)
        ],
        responses={201: openapi.Response(
            description="Sucsess"), 400: openapi.Response(description="Error")}
    )
    def post(self, request, format=None):  # 修正済み
        gamename = request.data.get("gamename")
        uid = request.data.get("uid")
        public = request.data.get("open")
        span = request.data.get("span")
        try:
            print(span)
            with transaction.atomic():
                game_rule = GameRule.objects.create(
                    start=span['start'],
                    end=span['end'],
                    open=public,
                    logic_id=999
                )

                game = Game.objects.create(
                    game_rule=game_rule,
                    name=gamename,
                )

                GamePlayer.objects.create(
                    game=game,
                    user=User.objects.filter(uid=uid).first()
                )
            return Response("Sucsess", status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)


class ApiGameView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uid', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='ユーザーID', required=True)
        ],
        responses={200: openapi.Response(
            description="ゲームリストの取得に成功"), 400: openapi.Response(description="不正なリクエスト")}
    )
    def get(self, request, uid, format=None):  # 修正済み
        try:
            user = User.objects.filter(uid=uid).first()
            gameplayers = GamePlayer.objects.filter(user=user)
            games = []
            for gameplayer in gameplayers:
                game_datamu = {
                    'id': gameplayer.game.id_for_serch,
                    'gamename': gameplayer.game.name,
                    'start': gameplayer.game.game_rule.start,
                    'end': gameplayer.game.game_rule.end, }

                games.append(game_datamu)

            return Response(games, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, gameid, format=None):  # 修正済み
        uid = request.data.get("uid")
        game = Game.objects.filter(id_for_serch=gameid).first()
        try:
            user = User.objects.filter(uid=uid).first()
            if game:
                game_player = GamePlayer.objects.filter(
                    game=game, user=user).first()
                if game_player:
                    return Response({"message": "既に参加しています"}, status=status.HTTP_200_OK)
                else:
                    GamePlayer.objects.create(
                        game=game,
                        user=user,
                    )
                    return Response({"message": "大会に参加しました"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "大会が存在しません"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, gameid, uid, format=None):  # 修正済み
        try:
            game_object = Game.objects.filter(id_for_serch=gameid).first()
            user_object = User.objects.filter(uid=uid).first()
            game_player = {'game': game_object, 'user': user_object}
            with transaction.atomic():
                GamePlayer.objects.filter(**game_player).delete()
                GameComment.objects.filter(**game_player).delete()
                Vote.objects.filter(**game_player).delete()
            return Response({"complete delete"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)


class APISarchGameView(APIView):
    def get(self, request, format=None):  # 修正済み
        try:
            gameserchid = request.query_params.get('gameserchid')
            print(gameserchid)

            def is_valid_uuid(val):
                try:
                    uuid.UUID(str(val))
                    return True
                except:
                    return False

            if is_valid_uuid(gameserchid):
                game = Game.objects.filter(id_for_serch=gameserchid).first()
                if game:
                    response = {
                        'id': game.id_for_serch,
                        "gamename": game.name
                    }
                else:
                    response = '大会が存在しません'
            else:
                response = '大会が存在しません'

            return Response({'message': response}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"message": '大会が存在しません'}, status=status.HTTP_400_BAD_REQUEST)


class APIScoreView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('gameid', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='ゲームID', required=True)
        ],
        responses={200: openapi.Response(description="スコアデータ取得に成功")}
    )
    def get(self, request, gameid, format=None):
        try:
            response_data = game_info(game_id=gameid)
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)


class ApiRaceView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('flag', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='フラグ', required=False),
            openapi.Parameter('uid', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='ユーザーID', required=True),
            openapi.Parameter('gameid', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='ゲームID', required=True)
        ],
        responses={200: openapi.Response(
            description="レース情報の取得に成功"), 400: openapi.Response(description="不正なリクエスト")}
    )
    def get(self, request, format=None):  # 修正済み
        try:
            flag = request.query_params.get('flag')
            if flag == '1':
                is_votables = [1, 2, 3]
            elif flag == "0":
                is_votables = [0]
            elif flag == "2":
                is_votables = [0, 1]
            uid = request.query_params.get('uid')
            gameid = request.query_params.get('gameid')
            start_date = Game.objects.filter(
                id_for_serch=gameid).first().game_rule.start
            end_date = Game.objects.filter(
                id_for_serch=gameid).first().game_rule.end
            print(start_date, end_date)
            game = Game.objects.filter(id_for_serch=gameid).first()
            user = User.objects.filter(uid=uid).first()
            voted_races = [
                vote.race for vote in Vote.objects.filter(user=user, game=game)]
            races = []
            for is_votable in is_votables:
                for race in Race.objects.filter(is_votable=is_votable, race_date__range=(start_date, end_date)):
                    datum = {}
                    Game.objects.filter
                    vote_num = race.vote_set.filter(game=game).count()

                    if race in voted_races:
                        datum = {"grade": race.rank,
                                 "name": race.race_name, "date": race.race_date, 'voted': True, "vote_num": vote_num, "is_votable": is_votable, "start_time": race.start_time}
                    else:
                        datum = {"grade": race.rank,
                                 "name": race.race_name, "date": race.race_date, 'voted': False, "vote_num": vote_num, "is_votable": is_votable, "start_time": race.start_time}

                    races.append(datum)

            races = sorted(races, key=lambda x: x["date"], reverse=True)
            compare_date = ''
            for race in races:
                if compare_date == race['date']:
                    race["isdisplay"] = False
                else:
                    race["isdisplay"] = True
                compare_date = race['date']
                print(races)

            return Response(races, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)


class ApiVoteView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('grade', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='レースのグレード', required=True),
            openapi.Parameter('date', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='レース日', required=True),
            openapi.Parameter('racename', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='レース名', required=True),
            openapi.Parameter('uid', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='ユーザーID', required=True),
            openapi.Parameter('gameid', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='ゲームID', required=True)
        ],
        responses={200: openapi.Response(description="投票データ取得に成功")}
    )
    def get(self, request, format=None):  # 修正済み
        print(9999999999999999999)
        try:
            grade = request.query_params.get('grade')
            date = request.query_params.get('date')
            race_name = request.query_params.get('racename')
            uid = request.query_params.get("uid")
            game_id = request.query_params.get('gameid')

            race = Race.objects.filter(
                rank=grade, race_date=date, race_name=race_name).first()

            horses = [{'id': horse.id, 'name': horse.horse_name}
                      for horse in Horse.objects.filter(race=race)]
            user = User.objects.filter(uid=uid).first()
            game = Game.objects.filter(id_for_serch=game_id).first()
            my_vote = Vote.objects.filter(
                user=user,
                race=race,
                game=game,
            ).first()
            vote_list = []

            for vote in Vote.objects.filter(game=game, race=race):

                user_name = vote.user.username
                votes = {"name": user_name,
                         "first": {'id': vote.horse_first.id, 'name': vote.horse_first.horse_name},
                         'second': {'id': vote.horse_second.id, 'name': vote.horse_second.horse_name},
                         "third": {'id': vote.horse_third.id, 'name': vote.horse_third.horse_name},
                         'comment': vote.comment}
                vote_list.append(votes)

            if my_vote:

                return Response({"vote": {
                    'first': my_vote.horse_first.id,
                    'second': my_vote.horse_second.id,
                    'third': my_vote.horse_third.id,
                    'comment': my_vote.comment},
                    "horses": horses,
                    "votelist": vote_list}, status=status.HTTP_200_OK)
            else:
                return Response({"vote": {
                    'first': None,
                    'second': None,
                    'third': None,
                    'comment': None},
                    "horses": horses,
                    "votelist": vote_list}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):  # 修正済み
        try:
            vote_form = request.data.get('voteForm')
            uid = request.data.get("uid")
            user = User.objects.filter(uid=uid).first()
            race_name = request.data.get("racename")
            game_id = request.data.get('gameid')
            race = Race.objects.filter(
                rank=race_name['grade'], race_date=race_name['date'], race_name=race_name['name']).first()
            game = Game.objects.filter(id_for_serch=game_id).first()
            if race.is_votable == 1:

                _, created = Vote.objects.update_or_create(
                    game=game,
                    race=race,
                    user=user,
                    defaults={
                        "horse_first": Horse.objects.get(id=vote_form['first']),
                        'horse_second': Horse.objects.get(id=vote_form['second']),
                        'horse_third': Horse.objects.get(id=vote_form['third']),
                        'comment': vote_form['comment'],
                    },
                )
                if created:
                    return Response({"sucsess": "投票しました"}, status=status.HTTP_200_OK)
                else:
                    return Response({"sucsess": "投票を更新しました"}, status=status.HTTP_200_OK)
            else:
                return Response({"sucsess": "投票は締め切られています"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)


class APIRaceResultView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('racename', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='レース名', required=True),
            openapi.Parameter('gameid', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, description='ゲームID', required=True)
        ],
        responses={200: openapi.Response(description="レース結果取得に成功")}
    )
    def get(self, request, racename, gameid, format=None):  # 修正済み
        try:
            race = Race.objects.filter(race_name=racename).first()
            horses = [{'id': horse.id, 'place': HorsePlace.objects.filter(horse=horse).first().place, 'name': horse.horse_name}
                      for horse in Horse.objects.filter(race=race)]
            horses = sorted(horses, key=lambda x: x["place"])
            game = Game.objects.filter(id_for_serch=gameid).first()

            odds = Odds.objects.filter(race=race).first()
            odds_datamu = {
                'tan': odds.tan,
                'fuku1': odds.fuku_1,
                'fuku2': odds.fuku_2,
                'fuku3': odds.fuku_3,
                'umaren': odds.umaren,
                'umatan': odds.umatan,
                'wide12': odds.wide_12,
                'wide13': odds.wide_13,
                'wide23': odds.wide_23,
                'trio': odds.trio,
                'tierce': odds.tierce
            }

            vote_list = []
            for vote in Vote.objects.filter(game=game, race=race):
                score = 0
                user_name = vote.user.username
                vote_1_place = HorsePlace.objects.filter(
                    horse=vote.horse_first).first().place
                vote_2_place = HorsePlace.objects.filter(
                    horse=vote.horse_second).first().place
                vote_3_place = HorsePlace.objects.filter(
                    horse=vote.horse_third).first().place
                votes = [vote_1_place, vote_2_place, vote_3_place]
                if vote_1_place == 1:
                    score += sum([odds_datamu['tan'], odds_datamu['fuku1']])
                if vote_1_place == 2:
                    score += odds_datamu['fuku2']

                if vote_1_place == 3:
                    score += odds_datamu['fuku3']
                if (vote_1_place*vote_2_place-2)*(vote_1_place*vote_3_place-2)*(vote_2_place*vote_3_place-2) == 0:
                    score += odds_datamu['umaren']
                if vote_1_place == 1 and vote_2_place == 2:
                    score += odds_datamu['umatan']
                if sum([1 for v in votes if v in [1, 2]]) >= 2:
                    score += odds_datamu['wide12']
                if sum([1 for v in votes if v in [1, 3]]) >= 2:
                    score += odds_datamu['wide13']
                if sum([1 for v in votes if v in [2, 3]]) >= 2:
                    score += odds_datamu['wide23']
                if sum(votes) == 6:
                    score += odds_datamu['trio']
                if [1, 2, 3] == votes:
                    score += odds_datamu['tierce']
                uid = vote.user.uid
                votes = {"name": user_name,
                         "UID": uid,
                         "first": {'place':  HorsePlace.objects.filter(horse=vote.horse_first).first().place, 'name': vote.horse_first.horse_name},
                         'second': {'place':  HorsePlace.objects.filter(horse=vote.horse_second).first().place, 'name': vote.horse_second.horse_name},
                         "third": {'place':  HorsePlace.objects.filter(horse=vote.horse_third).first().place, 'name': vote.horse_third.horse_name},
                         'comment': vote.comment,
                         'score': score}

                vote_list.append(votes)

            return Response({
                'body': {
                    'horses': horses,
                    'votes': vote_list,
                    'odds': odds_datamu,
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)
