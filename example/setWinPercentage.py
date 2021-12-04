from volleyball.stat.Chance import Chances
from volleyball.stat.StatMaker import *
from volleyball.scraper.LinkProcessor import LinkProcessor
from utills import make_percentage
from alive_progress import config_handler

config_handler.set_global(spinner="wait")


class ScoreAndWinPercentage:
    def __init__(self, scores, continuous_point):
        self.scores = tuple(scores)
        self.continuous_point = continuous_point
        self.set_result = [0, 0]

    def add_result(self, winner):
        self.set_result[winner] += 1


scores_and_win_percentages: Dict[tuple, List[int]] = {}
scores_and_win_percentages_five_set: Dict[tuple, List[int]] = {}

scores_and_win_percentages_1: List[ScoreAndWinPercentage] = []
scores_and_win_percentages_1_5th: List[ScoreAndWinPercentage] = []


def processor_in_set(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: Set):
    if set_in_game.index != 4:
        left_set_winner = (lambda scores: 0 if scores[0][set_in_game.index] > scores[1][set_in_game.index] else 1)(
            game.scores)
        right_set_winner = (lambda right_winner: 0 if left_set_winner == 1 else 1)(left_set_winner)
        left_continuous_point = 0
        for rally in rallies:
            if tuple(rally.score) in map(lambda score_and_win_percentage: score_and_win_percentage.scores,
                                         scores_and_win_percentages_1):
                for score_and_win_percentage_one in scores_and_win_percentages_1:
                    if score_and_win_percentage_one.scores == tuple(
                            rally.score) and score_and_win_percentage_one.continuous_point == left_continuous_point:
                        score_and_win_percentage_one.add_result(left_set_winner)
            else:
                scores_and_win_percentages_1.append(ScoreAndWinPercentage(rally.score, left_continuous_point))
                scores_and_win_percentages_1[len(scores_and_win_percentages_1) - 2].add_result(left_set_winner)

            rally.score.reverse()

            if tuple(rally.score) in map(lambda score_and_win_percentage: score_and_win_percentage.scores,
                                         scores_and_win_percentages_1):
                for score_and_win_percentage_one in scores_and_win_percentages_1:
                    if score_and_win_percentage_one.scores == tuple(
                            rally.score) and score_and_win_percentage_one.continuous_point == -left_continuous_point:
                        score_and_win_percentage_one.add_result(right_set_winner)
            else:
                scores_and_win_percentages_1.append(ScoreAndWinPercentage(rally.score, -left_continuous_point))
                scores_and_win_percentages_1[len(scores_and_win_percentages_1) - 2].add_result(right_set_winner)

            if left_continuous_point > 0 and rally.winner == 1:
                left_continuous_point = -1
            elif left_continuous_point < 0 and rally.winner == 0:
                left_continuous_point = 1
            elif rally.winner == 0:
                left_continuous_point += 1
            else:
                left_continuous_point -= 1

    else:
        left_set_winner = (lambda scores: 0 if scores[0][set_in_game.index] > scores[1][set_in_game.index] else 1)(
            game.scores)
        right_set_winner = (lambda right_winner: 0 if left_set_winner == 1 else 1)(left_set_winner)
        left_continuous_point = 0
        for rally in rallies:
            if tuple(rally.score) in map(lambda score_and_win_percentage: score_and_win_percentage.scores,
                                         scores_and_win_percentages_1_5th):
                for score_and_win_percentage_one in scores_and_win_percentages_1_5th:
                    if score_and_win_percentage_one.scores == tuple(
                            rally.score) and score_and_win_percentage_one.continuous_point == left_continuous_point:
                        score_and_win_percentage_one.add_result(left_set_winner)
            else:
                scores_and_win_percentages_1_5th.append(ScoreAndWinPercentage(rally.score, left_continuous_point))
                scores_and_win_percentages_1_5th[len(scores_and_win_percentages_1_5th) - 2].add_result(left_set_winner)

            rally.score.reverse()

            if tuple(rally.score) in map(lambda score_and_win_percentage: score_and_win_percentage.scores,
                                         scores_and_win_percentages_1_5th):
                for score_and_win_percentage_one in scores_and_win_percentages_1_5th:
                    if score_and_win_percentage_one.scores == tuple(
                            rally.score) and score_and_win_percentage_one.continuous_point == -left_continuous_point:
                        score_and_win_percentage_one.add_result(right_set_winner)
            else:
                scores_and_win_percentages_1_5th.append(ScoreAndWinPercentage(rally.score, -left_continuous_point))
                scores_and_win_percentages_1_5th[len(scores_and_win_percentages_1_5th) - 2].add_result(right_set_winner)

            if left_continuous_point > 0 and rally.winner == 1:
                left_continuous_point = -1
            elif left_continuous_point < 0 and rally.winner == 0:
                left_continuous_point = 1
            elif rally.winner == 0:
                left_continuous_point += 1
            else:
                left_continuous_point -= 1


link_processor = LinkProcessor(
    [LinkProcessor.WOMEN],
    [LinkProcessor.REGULAR_SEASON, LinkProcessor.PLAY_OFF, LinkProcessor.SEMI_PLAY_OFF, LinkProcessor.CHAMP]
    , list(range(2020, 2021))
    , list(range(1, 30)))
link_processor.make_round_number()
stat = Stat(link_processor.links)

stat.fill_games()
stat.fill_sets()
stat.fill_messages()
stat.fill_rallies()
stat.fill_chances()

stat.process_in_set(processor_in_set)

for score_and_win_percentage_1 in scores_and_win_percentages_1:
    print(score_and_win_percentage_1.__dict__,
          make_percentage(score_and_win_percentage_1.set_result[0] + score_and_win_percentage_1.set_result[1]
                          , score_and_win_percentage_1.set_result[0] - score_and_win_percentage_1.set_result[1]))

for score_and_win_percentage_1_5th in scores_and_win_percentages_1_5th:
    print(score_and_win_percentage_1_5th.__dict__,
          make_percentage(score_and_win_percentage_1_5th.set_result[0] + score_and_win_percentage_1_5th.set_result[1]
                          , score_and_win_percentage_1_5th.set_result[0] - score_and_win_percentage_1_5th.set_result[1]))
