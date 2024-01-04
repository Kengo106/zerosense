from .models import Race, HorsePlace, Odds, Vote, Game, GamePlayer
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q

# game_idにリレーションのあるデータを取得する


def get_game_related_info(game_id):
    game = Game.objects.filter(id=game_id).prefetch_related(
        'gameplayers_set__user',
        'vote_set__race',
        'vote_set__race__odds',
        'vote_set__user',
        'vote_set__horse_first',
        'vote_set__horse_second',
        'vote_set__horse_third',
        'vote_set__horse_first__horseplace',
        'vote_set__horse_second__horseplace',
        'vote_set__horse_third__horseplace',
    )

    return game


# どの馬券が当たったかを判定する

def judge_hit(votes):
    '''
    scores = [tan,fuku1,fuku2,fuku3,umaren,umatan,wide12,wide13,wide23,trio,teirce]
    '''

    scores = []

    scores.append(votes[0] == 1)  # tan
    scores.append(votes[0] == 1)  # fuku1
    scores.append(votes[0] == 2)  # fuku2
    scores.append(votes[0] == 3)  # fuku3
    scores.append((votes[0]*votes[1]-2)*(votes[0] *
                                         votes[2]-2)*(votes[1]*votes[2]-2) == 0)  # umaren
    scores.append(votes[0] == 1 and votes[1] == 2)  # umatan
    scores.append(sum([1 for v in votes if v in [1, 2]]) >= 2)  # wide12
    scores.append(sum([1 for v in votes if v in [1, 3]]) >= 2)  # wide13
    scores.append(sum([1 for v in votes if v in [2, 3]]) >= 2)  # wide23
    scores.append(sum(votes) == 6)  # trio
    scores.append([1, 2, 3] == votes)  # tierce

    return scores

# レースのオッズを取得する


def get_odds(race):

    odds_object = Odds.objects.filter(
        race=race).first()  # 払戻金を取得

    odds_list = []
    odds_list.append(odds_object.tan)
    odds_list.append(odds_object.fuku_1)
    odds_list.append(odds_object.fuku_2)
    odds_list.append(odds_object.fuku_3)
    odds_list.append(odds_object.umaren)
    odds_list.append(odds_object.umatan)
    odds_list.append(odds_object.wide_12)
    odds_list.append(odds_object.wide_13)
    odds_list.append(odds_object.wide_23)
    odds_list.append(odds_object.trio)
    odds_list.append(odds_object.tierce)

    return odds_list

# 今週のレースかを判定する


def is_latest_week_race(race_id):
    latest_race = Race.objects.filter(
        is_votable=0).order_by('-race_date').first()

    if latest_race:
        end_date = latest_race.race_date
        start_date = end_date - timedelta(days=3)
        latest_week_race = Race.objects.filter(
            race_date__range=(start_date, end_date))

    is_latest_week_race = False
    if latest_week_race.filter(id=race_id).exists():
        is_latest_week_race = True

    return is_latest_week_race


def calc_last_week_score(player_object):

    game_object = player_object.game
    vote_objects = Vote.objects.filter(
        game=game_object, user=player_object.user).order_by('-created_at')

    last_week_score = 0

    for vote_object in vote_objects:  # 各参加者のraceごとの投票を取得
        if Odds.objects.filter(race=vote_object.race).exists():
            scores = []
            if is_latest_week_race(vote_object.race.id):
                odds_list = get_odds(race=vote_object.race)
                if HorsePlace.objects.filter(horse=vote_object.horse_first).first():
                    vote_1_place = HorsePlace.objects.filter(
                        horse=vote_object.horse_first).first().place
                    vote_2_place = HorsePlace.objects.filter(
                        horse=vote_object.horse_second).first().place
                    vote_3_place = HorsePlace.objects.filter(
                        horse=vote_object.horse_third).first().place
                    votes = [vote_1_place, vote_2_place, vote_3_place]

                    hit_list = judge_hit(votes)
                    scores = [a*b for a, b in zip(hit_list, odds_list)]
                last_week_score += sum(scores)

    return last_week_score

# 的中回数、投票回数を計算する


def calc_hit_time(player_object):
    game_object = player_object.game
    vote_objects = Vote.objects.filter(
        game=game_object, user=player_object.user).order_by('-created_at')
    time_datamu = {}
    tan_time = 0
    fuku_time = 0
    umaren_time = 0
    umatan_time = 0
    wide_time = 0
    trio_time = 0
    tierce_time = 0
    million_time = 0
    vote_time = 0

    for vote_object in vote_objects:  # 各参加者のraceごとの投票を取得
        if Odds.objects.filter(race=vote_object.race).exists():
            odds_list = get_odds(race=vote_object.race)
            vote_time += 1
            if HorsePlace.objects.filter(horse=vote_object.horse_first).first():
                vote_1_place = HorsePlace.objects.filter(
                    horse=vote_object.horse_first).first().place
                vote_2_place = HorsePlace.objects.filter(
                    horse=vote_object.horse_second).first().place
                vote_3_place = HorsePlace.objects.filter(
                    horse=vote_object.horse_third).first().place
                votes = [vote_1_place, vote_2_place, vote_3_place]

                hit_list = judge_hit(votes)
                scores = [a*b for a, b in zip(hit_list, odds_list)]

            tan_time += hit_list[0]
            fuku_time += sum(hit_list[1:4])
            umaren_time += hit_list[4]
            umatan_time += hit_list[5]
            wide_time += sum(hit_list[6:9])
            trio_time += hit_list[9]
            tierce_time += hit_list[10]
            million_time += sum(
                1 for ticket in scores if int(ticket) >= 10000)
    time_datamu['tan_time'] = tan_time
    time_datamu['fuku_time'] = fuku_time
    time_datamu['umaren_time'] = umaren_time
    time_datamu['umatan_time'] = umatan_time
    time_datamu['wide_time'] = wide_time
    time_datamu['trio_time'] = trio_time
    time_datamu['tierce_time'] = tierce_time
    time_datamu['million_time'] = million_time
    time_datamu['vote_time'] = vote_time

    return time_datamu

# 月ごとのスコアを算出する


def calc_monthly_socere(player_object):
    game_object = player_object.game
    vote_objects = Vote.objects.filter(
        game=game_object, user=player_object.user).order_by('-created_at')

    game_span_month = calc_game_span_month(game_object=game_object)

    monthly_datam = {}

    for game_month in game_span_month:
        month_key = f'{game_month.year}-{game_month.month}'
        monthly_datam[month_key] = 0  # キーを初期化
        month_vote_objects = vote_objects.filter(Q(race__race_date__lt=game_month + relativedelta(months=1)) &
                                                 Q(race__race_date__gte=game_month))

        for vote_object in month_vote_objects:  # 各参加者のraceごとの投票を取得
            if Odds.objects.filter(race=vote_object.race).exists():

                odds_list = get_odds(race=vote_object.race)
                scores = []
                if HorsePlace.objects.filter(horse=vote_object.horse_first).first():
                    vote_1_place = HorsePlace.objects.filter(
                        horse=vote_object.horse_first).first().place
                    vote_2_place = HorsePlace.objects.filter(
                        horse=vote_object.horse_second).first().place
                    vote_3_place = HorsePlace.objects.filter(
                        horse=vote_object.horse_third).first().place
                    votes = [vote_1_place, vote_2_place, vote_3_place]

                    hit_list = judge_hit(votes)
                    scores = [a*b for a, b in zip(hit_list, odds_list)]

                    monthly_datam[month_key] += sum(scores)

    return monthly_datam


def calc_game_span_month(game_object):
    start_date = game_object.game_rule.start
    end_date = game_object.game_rule.end
    date_tmp = start_date.replace(day=1)
    game_span_month = []

    while date_tmp <= end_date:
        game_span_month.append(date_tmp)
        date_tmp += relativedelta(months=1)
    print(game_span_month)

    return game_span_month


def game_info(game_id):
    game_object = Game.objects.filter(id_for_serch=game_id).first()
    player_objects = GamePlayer.objects.filter(game=game_object)
    game_information = []

    user_monthly_score_dict = {}
    for player_object in player_objects:
        player_data = {}
        hit_time_dict = calc_hit_time(player_object=player_object)
        last_week_score = calc_last_week_score(player_object=player_object)
        monthly_score_dict = calc_monthly_socere(player_object=player_object)
        user_monthly_score_dict[player_object.user.username] = monthly_score_dict

        player_data = {
            'name': player_object.user.username,
            'vote_time': hit_time_dict['vote_time'],
            'nowscore': sum(monthly_score_dict.values()),  # 月ごとのスコアの合計
            'recovery_rate': int(sum(monthly_score_dict.values())/(11*hit_time_dict['vote_time'])) if hit_time_dict['vote_time'] else 0,
            'latest_week_race_score': last_week_score,
            'tan_time': hit_time_dict['tan_time'],
            'fuku_time': hit_time_dict['fuku_time'],
            'umaren_time': hit_time_dict['umaren_time'],
            'umatan_time': hit_time_dict['umatan_time'],
            'wide_time': hit_time_dict['wide_time'],
            'trio_time': hit_time_dict['trio_time'],
            'tierce_time': hit_time_dict['tierce_time'],
            'million_time': hit_time_dict['million_time'],

        }

        game_information.append(player_data)

    game_span_month = calc_game_span_month(game_object=game_object)
    month_top_scores = []
    for game_month in game_span_month:
        month_key = f'{game_month.year}-{game_month.month}'
        top_scorers = []
        top_score = 0
        for player_object in player_objects:
            player_score = user_monthly_score_dict[player_object.user.username][month_key]
            if top_score < player_score:
                top_scorers = [player_object.user.username]
                top_score = player_score
            elif top_score == player_score and player_score != 0:
                top_scorers.append(player_object.user.username)
            print(month_key, top_scorers, top_score)
        for top_scorer in top_scorers:
            month_top_scores.append(top_scorer)
    print(month_top_scores)

    game_information = sorted(
        game_information, key=lambda x: x['nowscore'], reverse=True)

    # ランキング位置を更新
    for index, info in enumerate(game_information):
        info['place'] = index + 1
        info['get_top_in_month'] = sum(
            [1 for i in month_top_scores if i == info['name']])

    return game_information
