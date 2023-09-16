from ..models import User, Game, GameRule, GamePlayer, GameComment, Race, Horse, Vote, Odds, HorsePlace
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Subquery, OuterRef
from django_filters import rest_framework as filters
from rest_framework import status
from django.db import transaction
import traceback
from datetime import timedelta
from django.db.models.functions import ExtractMonth


def game_score(request):
    # return{username:{racename:score}}

    game = request.query_params.get("game")
    game_object = Game.objects.filter(name=game).first()
    game_player_objects = GamePlayer.objects.filter(Game=game_object)
    user_datamu = {}
    temporary_month_datamu = {}
    game_infomation = []
    latest_week_race_score_datamu = {}
    hit_time_datamu = {}
    latest_race = Race.objects.filter(
        is_votable=0).order_by('-race_date').first()

    if latest_race:
        end_date = latest_race.race_date
        start_date = end_date - timedelta(days=3)
        latest_week_race = Race.objects.filter(
            race_date__range=(start_date, end_date))
        for rname, date in zip([race.race_name for race in latest_week_race], [race.race_date for race in latest_week_race]):
            print(rname, date)
    for game_player_object in game_player_objects:  # 各ゲームの参加者を取得
        vote_objects = Vote.objects.filter(
            game=game_object, user=game_player_object.User).order_by('-created_at')
        score_datamu = {}
        month_datamu = {}
        latest_week_race_score = 0
        time_datamu = {}
        tan_time = 0
        fuku_time = 0
        umaren_time = 0
        umatan_time = 0
        wide_time = 0
        trio_time = 0
        tierce_time = 0
        get_scores = []
        for vote_object in vote_objects:  # 各参加者のraceごとの投票を取得
            score = 0
            odds_object = Odds.objects.filter(
                Race=vote_object.race).first()  # 各レースの払戻金を取得
            is_latest_week_race = False
            month = vote_object.race.race_date.month
            month_datamu[month] = 0

            if latest_week_race.filter(id=vote_object.race.id).exists():
                is_latest_week_race = True
            if HorsePlace.objects.filter(Horse=vote_object.horse_first).first():
                vote_1_place = HorsePlace.objects.filter(
                    Horse=vote_object.horse_first).first().place
                vote_2_place = HorsePlace.objects.filter(
                    Horse=vote_object.horse_second).first().place
                vote_3_place = HorsePlace.objects.filter(
                    Horse=vote_object.horse_third).first().place
                votes = [vote_1_place, vote_2_place, vote_3_place]
                if vote_1_place == 1:
                    score += sum([odds_object.tan, odds_object.fuku_1])
                    tan_time += 1
                    fuku_time += 1
                    get_scores.append(odds_object.fuku_1)
                    get_scores.append(odds_object.tan)
                    if is_latest_week_race:
                        latest_week_race_score += sum(
                            [odds_object.tan, odds_object.fuku_1])
                if vote_1_place == 2:
                    score += odds_object.fuku_2
                    fuku_time += 1
                    get_scores.append(odds_object.fuku_2)
                    if is_latest_week_race:
                        latest_week_race_score += odds_object.fuku_2
                if vote_1_place == 3:
                    score += odds_object.fuku_3
                    fuku_time += 1
                    get_scores.append(odds_object.fuku_3)
                    if is_latest_week_race:
                        latest_week_race_score += odds_object.fuku_3
                if (vote_1_place*vote_2_place-2)*(vote_1_place*vote_3_place-2)*(vote_2_place*vote_3_place-2) == 0:
                    score += odds_object.umaren
                    umaren_time += 1
                    get_scores.append(odds_object.umaren)
                    if is_latest_week_race:
                        latest_week_race_score += odds_object.umaren
                if vote_1_place == 1 and vote_2_place == 2:
                    score += odds_object.umatan
                    umatan_time += 1
                    get_scores.append(odds_object.umatan)
                    if is_latest_week_race:
                        latest_week_race_score += odds_object.umatan
                if sum([1 for v in votes if v in [1, 2]]) >= 2:
                    score += odds_object.wide_12
                    wide_time += 1
                    get_scores.append(odds_object.wide_12)
                    if is_latest_week_race:
                        latest_week_race_score += odds_object.wide_12
                if sum([1 for v in votes if v in [1, 3]]) >= 2:
                    score += odds_object.wide_13
                    get_scores.append(odds_object.wide_13)
                    wide_time += 1
                    if is_latest_week_race:
                        latest_week_race_score += odds_object.wide_13
                if sum([1 for v in votes if v in [2, 3]]) >= 2:
                    score += odds_object.wide_23
                    wide_time += 1
                    get_scores.append(odds_object.wide_23)
                    if is_latest_week_race:
                        latest_week_race_score += odds_object.wide_23
                if sum(votes) == 6:
                    score += odds_object.trio
                    trio_time += 1
                    get_scores.append(odds_object.trio)
                    if is_latest_week_race:
                        latest_week_race_score += odds_object.trio
                if [1, 2, 3] == votes:
                    score += odds_object.tierce
                    tierce_time += 1
                    get_scores.append(odds_object.tierce)
                    if is_latest_week_race:
                        latest_week_race_score += odds_object.tierce
                score_datamu[f'{vote_object.race.race_name}'] = score
                month_datamu[month] = month_datamu[month]+score
        time_datamu['tan_time'] = tan_time
        time_datamu['fuku_time'] = fuku_time
        time_datamu['umaren_time'] = umaren_time
        time_datamu['umatan_time'] = umatan_time
        time_datamu['wide_time'] = wide_time
        time_datamu['trio_time'] = trio_time
        time_datamu['tierce_time'] = tierce_time
        time_datamu['million_time'] = sum(
            1 for ticket in get_scores if int(ticket) >= 10000)
        latest_week_race_score_datamu[game_player_object.User.username] = latest_week_race_score
        hit_time_datamu[game_player_object.User.username] = time_datamu
        user_datamu[game_player_object.User.username] = score_datamu
        temporary_month_datamu[game_player_object.User.username] = month_datamu
    print(temporary_month_datamu)

    month_score_datamu = {}
    for name, scores in temporary_month_datamu.items():
        for key, score in scores.items():
            if type(key) == int:
                if key not in month_score_datamu.keys():
                    month_score_datamu[key] = {}
                month_score_datamu[key][name] = score
    calculate_get_month_top = []
    for key, player_score in month_score_datamu.items():
        max_score = max(player_score.values())
        for name, score in player_score.items():
            if score == max_score:
                calculate_get_month_top.append(name)

    print(calculate_get_month_top.count("Kengo"))

    for game_player_object in game_player_objects:
        name = game_player_object.User.username
        temporary_datamu = {}
        print(user_datamu)
        score = sum(
            user_datamu[name].values())
        vote_time = len(user_datamu[name])
        print(user_datamu)

        recovery_rate = int(score / (11*vote_time))
        player_hit_info = hit_time_datamu[name]
        temporary_datamu.update({
            'name': name,
            'vote_time': vote_time,
            'nowscore': score,
            'recovery_rate': recovery_rate,
            'latest_week_race_score': latest_week_race_score_datamu[name],
            "tan_time": player_hit_info['tan_time'],
            "fuku_time": player_hit_info['fuku_time'],
            "umaren_time": player_hit_info['umaren_time'],
            "umatan_time": player_hit_info['umatan_time'],
            "wide_time": player_hit_info['wide_time'],
            "trio_time": player_hit_info['trio_time'],
            "tierce_time": player_hit_info['tierce_time'],
            "million_time": player_hit_info['million_time'],
            'get_top_in_month': calculate_get_month_top.count(name)

        })

        game_infomation.append(temporary_datamu)
    game_infomation = sorted(
        game_infomation, key=lambda x: x["nowscore"], reverse=True)
    response_data = []
    for index, info in enumerate(game_infomation):
        info["place"] = index + 1
        response_data.append(info)
    return user_datamu, response_data


class ApiUIDView(APIView):
    def post(self, request, format=None):
        uid = request.data.get('uid')
        username = request.data.get('username')
        try:
            User.objects.create(
                UID=uid,
                username=username
            )
            response = Response(
                {"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        except:
            response = Response({"message": "miss"},
                                status=status.HTTP_400_BAD_REQUEST)

        return response


class ApiNewGameView(APIView):
    def post(self, request, format=None):
        gamename = request.data.get("gamename")
        uid = request.data.get("uid")
        public = request.data.get("open")
        span = request.data.get("span")
        try:
            with transaction.atomic():
                game_rule = GameRule.objects.create(
                    span=span,
                    open=public,
                    logic_id=999
                )

                game = Game.objects.create(
                    GameRule=game_rule,
                    name=gamename,
                )

                GamePlayer.objects.create(
                    Game=game,
                    User=User.objects.filter(UID=uid).first()
                )
            return Response("Sucsess", status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)


class ApiJoinGameView(APIView):
    def get(self, request, format=None):
        try:
            uid = request.query_params.get("uid")
            user = User.objects.filter(UID=uid).first()
            gameplayers = GamePlayer.objects.filter(User=user)
            gamenames = []
            for gameplayer in gameplayers:
                gamenames.append(gameplayer.Game.name)

            return Response(gamenames, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        gamename = request.data.get("gamename")
        uid = request.data.get("uid")
        game = Game.objects.filter(name=gamename).first()
        try:
            user = User.objects.filter(UID=uid).first()
            if game:
                game_player = GamePlayer.objects.filter(
                    Game=game, User=user).first()
                if game_player:
                    return Response({"message": "既に参加しています"}, status=status.HTTP_200_OK)
                else:
                    GamePlayer.objects.create(
                        Game=game,
                        User=user,
                    )
                    return Response({"message": "大会に参加しました"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "大会が存在しません"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)


class ApiRaceView(APIView):
    def get(self, request, format=None):
        try:
            flag_before = request.query_params.get('flag')
            if flag_before == '1':
                flags = [1]
            elif flag_before == "0":
                flags = [0]
            elif flag_before == "2":
                flags = [0, 1]
            uid = request.query_params.get('uid')
            user = User.objects.filter(UID=uid).first()
            voted_races = [
                vote.race for vote in Vote.objects.filter(user=user)]
            races = []
            for flag in flags:
                for race in Race.objects.filter(is_votable=flag):
                    datum = {}
                    if race in voted_races:
                        datum = {"grade": race.rank,
                                 "name": race.race_name, "date": race.race_date, 'voted': True}
                    else:
                        datum = {"grade": race.rank,
                                 "name": race.race_name, "date": race.race_date, 'voted': False}

                    races.append(datum)

            return Response(races, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)


class ApiVoteView(APIView):
    def get(self, request, format=None):
        try:
            grade = request.query_params.get('grade')
            date = request.query_params.get('date')
            race_name = request.query_params.get('name')
            uid = request.query_params.get("uid")
            game_name = request.query_params.get('gamename')
            race = Race.objects.filter(
                rank=grade, race_date=date, race_name=race_name).first()
            horses = [{'id': horse.id, 'name': horse.horse_name}
                      for horse in Horse.objects.filter(Race_id=race)]
            user = User.objects.filter(UID=uid).first()
            game = Game.objects.filter(name=game_name).first()
            my_vote = Vote.objects.filter(
                user=user,
                race=race,
                game=game,
            ).first()
            vote_list = []

            for vote in Vote.objects.filter(game=game, race=race):
                # user_name = User.objects.filter(id=vote.user).first()
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

    def post(self, request, format=None):
        try:
            vote_form = request.data.get('voteForm')
            uid = request.data.get("uid")
            user = User.objects.filter(UID=uid).first()
            race_name = request.data.get("racename")
            game_name = request.data.get('game')
            race = Race.objects.filter(
                rank=race_name['grade'], race_date=race_name['date'], race_name=race_name['name']).first()
            game = Game.objects.filter(name=game_name).first()

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
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)


class APIScoreView(APIView):
    def get(self, request, format=None):
        try:
            _, response_data = game_score(request=request)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)


class APIUserNameView(APIView):
    def put(self, request, format=None):
        try:
            update_name = request.data.get('name')
            UID = request.data.get('uid')
            User.objects.filter(UID=UID).update(username=update_name)
            return Response({"message": f'変更しました： {update_name}'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error occurred: {e}")  # エラーメッセージを表示
            traceback.print_exc()
            return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)
