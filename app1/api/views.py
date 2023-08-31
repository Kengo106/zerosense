from ..models import RaceResult, Odds, JoinResultOdds, User, Game, GameRule, GamePlayer, GameComment, Race, Horse, Vote
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RaceResultSeriralizer, OddsSerilizer, RacenameSerializer, JoinResultOddsSerializer
from django.db.models import Subquery, OuterRef
from django_filters import rest_framework as filters
from rest_framework import status
from django.db import transaction
import traceback


class ApiRaceView(APIView):

    def get(self, request, format=None):
        return Response({"response": "GET RESULT recently 10 records"})

    def post(self, request, format=None):
        race_results = RaceResult.objects.order_by("-created_at").all()[:10]
        serialized_data_list = []
        for race_result in race_results:
            Serializer = RaceResultSeriralizer(race_result)
            serialized_data_list.append(Serializer.data)

        return Response(serialized_data_list)


class ApiOddsView(APIView):

    def get(self, request, format=None):
        return Response({"response": "GET ODDS recently 10 records"})

    def post(self, request, format=None):
        odds_results = Odds.objects.order_by('-created_at').all()[:10]
        serialized_data_list = []
        for odds_result in odds_results:
            Serializer = OddsSerilizer(odds_result)
            serialized_data_list.append(Serializer.data)

        return Response(serialized_data_list)


class ApiRaceNameView(APIView):

    def get(self, request, format=None):
        distinct_race_ids = RaceResult.objects.order_by(
            'race_name', '-created_at').distinct('race_name').values('id')
        race_names = RaceResult.objects.filter(id__in=Subquery(
            distinct_race_ids)).order_by('-created_at')
        serializer = RacenameSerializer(race_names, many=True)
        return Response(serializer.data)


class FilterResult(filters.FilterSet):
    class Meta:
        model = RaceResult
        fields = '__all__'


class FilterOdds(filters.FilterSet):
    class Meta:
        model = Odds
        fields = '__all__'


class FilterJoinResultOdds(filters.FilterSet):
    class Meta:
        model = JoinResultOdds
        fields = "__all__"


class ApiResultOddsview(APIView):
    def get(self, request, format=None):
        filterresult = FilterResult(
            request.query_params, queryset=RaceResult.objects.all())
        filterodds = FilterOdds(request.query_params,
                                queryset=Odds.objects.all())
        result_serializer = RaceResultSeriralizer(
            instance=filterresult.qs, many=True)
        odds_serializer = OddsSerilizer(instance=filterodds.qs, many=True)
        return Response({
            "result": result_serializer.data,
            "odds": odds_serializer.data
        })


class ApiJoinView(APIView):
    def get(self, request, format=None):
        race_name = request.query_params.get("race_name")
        join_query = JoinResultOdds.objects.select_related(
            'RaceResult', "Odds").filter(RaceResult__race_name=race_name)
        join_serializer = JoinResultOddsSerializer(
            instance=join_query, many=True)
        return Response(join_serializer.data)


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
        print(gamename, uid, type(public), span)
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
            flag = request.query_params.get('flag')
            races = [{"grade": race.rank, "name": race.race_name, "date": race.race_date}
                     for race in Race.objects.filter(is_votable=flag)]

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

                print("Vote exists!")
                print("Vote details:")
                print(f"horse_first: {vote.horse_first.id}")
                print(f"horse_second: {vote.horse_second.id}")
                print(f"horse_third: {vote.horse_third.id}")
                for horse in horses:
                    print(horse)
                print(f"comment: {vote.comment}")
                # ... 以降のコード

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
