from .models import Race, HorsePlace, Odds, Vote, Game, GamePlayer
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q

# game_idにリレーションのあるデータを取得する


def get_game_related_info(game_id):
    game = Game.objects.select_related(
        'game_rule'
    ).prefetch_related(
        'gameplayer_set__user',
        'vote_set__race',
        'vote_set__race__odds',
        'vote_set__user',
        'vote_set__horse_first',
        'vote_set__horse_second',
        'vote_set__horse_third',
        'vote_set__horse_first__horseplace',
        'vote_set__horse_second__horseplace',
        'vote_set__horse_third__horseplace',
    ).get(id_for_search=game_id)

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


def get_odds(odds):

    # odds_object = race.odds  # 払戻金を取得

    odds_list = []
    odds_list.append(odds.tan)
    odds_list.append(odds.fuku_1)
    odds_list.append(odds.fuku_2)
    odds_list.append(odds.fuku_3)
    odds_list.append(odds.umaren)
    odds_list.append(odds.umatan)
    odds_list.append(odds.wide_12)
    odds_list.append(odds.wide_13)
    odds_list.append(odds.wide_23)
    odds_list.append(odds.trio)
    odds_list.append(odds.tierce)

    return odds_list

# 今週のレースかを判定する


def is_latest_week_race(race_id, game):
    latest_date = None

    for vote in game.vote_set.all():
        if vote.race.id == race_id:
            race_date = vote.race.race_date
        if vote.race.is_votable == 0 and (latest_date is None or (vote.race.race_date > latest_date)):
            latest_date = vote.race.race_date

    return race_date > latest_date - timedelta(days=4)


#  最新のレースから3日以内のレースのスコアを計算する
def calc_last_week_score(player_instance, game):

    vote_instances = player_instance.user.vote_set.all()  # Corrected here
    last_week_score = 0

    for vote_instance in vote_instances:  # 各参加者のraceごとの投票を取得
        race = vote_instance.race
        if hasattr(race, 'odds'):  # oddsが取得済みのレースのみ対象  # Corrected here
            scores = []
            if is_latest_week_race(vote_instance.race.id, game=game):
                odds = race.odds
                odds_list = get_odds(odds=odds)

                if vote_instance.horse_first.horseplace:
                    vote_1_place = vote_instance.horse_first.horseplace.place
                    vote_2_place = vote_instance.horse_second.horseplace.place
                    vote_3_place = vote_instance.horse_third.horseplace.place
                    votes = [vote_1_place, vote_2_place, vote_3_place]
                    hit_list = judge_hit(votes)
                    scores = [a*b for a, b in zip(hit_list, odds_list)]

                    last_week_score += sum(scores)

    return last_week_score

# 的中回数、投票回数を計算する


def calc_hit_time(player_instance):
    vote_instances = player_instance.user.vote_set.all()  # Corrected here
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

    for vote_instance in vote_instances:  # 各参加者のraceごとの投票を取得
        race = vote_instance.race
        if hasattr(race, 'odds'):  # oddsが取得済みのレースのみ対象  # Corrected here
            odds = race.odds
            odds_list = get_odds(odds=odds)
            vote_time += 1
            if vote_instance.horse_first.horseplace:
                vote_1_place = vote_instance.horse_first.horseplace.place
                vote_2_place = vote_instance.horse_second.horseplace.place
                vote_3_place = vote_instance.horse_third.horseplace.place
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


def calc_monthly_socere(player_instance, game):
    vote_instances = player_instance.user.vote_set.all()
    game_span_month = calc_game_span_month(game=game)

    monthly_datam = {}

    for game_month in game_span_month:
        month_key = f'{game_month.year}-{game_month.month}'
        monthly_datam[month_key] = 0  # キーを初期化
        month_vote_instances = vote_instances.filter(Q(race__race_date__lt=game_month + relativedelta(months=1)) &
                                                     Q(race__race_date__gte=game_month))

        for vote_instance in month_vote_instances:  # 各参加者のraceごとの投票を取得
            race = vote_instance.race  # oddsを取得するため
            if hasattr(race, 'odds'):  # oddsが取得済みのレースのみ対象
                odds = race.odds
                odds_list = get_odds(odds=odds)
                if vote_instance.horse_first.horseplace:
                    vote_1_place = vote_instance.horse_first.horseplace.place
                    vote_2_place = vote_instance.horse_second.horseplace.place
                    vote_3_place = vote_instance.horse_third.horseplace.place
                    votes = [vote_1_place, vote_2_place, vote_3_place]

                    hit_list = judge_hit(votes)
                    scores = [a*b for a, b in zip(hit_list, odds_list)]

                    monthly_datam[month_key] += sum(scores)

    return monthly_datam


def calc_game_span_month(game):
    start_date = game.game_rule.start
    end_date = game.game_rule.end
    date_tmp = start_date.replace(day=1)
    game_span_month = []

    while date_tmp <= end_date:
        game_span_month.append(date_tmp)
        date_tmp += relativedelta(months=1)
    print(game_span_month)

    return game_span_month


def game_info(game_id):

    game = get_game_related_info(game_id)
    player_instances = game.gameplayer_set.all()
    game_information = []

    user_monthly_score_dict = {}
    for player_instance in player_instances:
        player_data = {}
        hit_time_dict = calc_hit_time(
            player_instance=player_instance)
        last_week_score = calc_last_week_score(
            player_instance=player_instance, game=game)
        monthly_score_dict = calc_monthly_socere(
            player_instance=player_instance, game=game)
        user_monthly_score_dict[player_instance.user.username] = monthly_score_dict

        player_data = {
            'name': player_instance.user.username,
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

    game_span_month = calc_game_span_month(game=game)
    month_top_scores = []
    for game_month in game_span_month:
        month_key = f'{game_month.year}-{game_month.month}'
        top_scorers = []
        top_score = 0
        for player_instance in player_instances:
            player_score = user_monthly_score_dict[player_instance.user.username][month_key]
            if top_score < player_score:
                top_scorers = [player_instance.user.username]
                top_score = player_score
            elif top_score == player_score and player_score != 0:
                top_scorers.append(player_instance.user.username)
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
