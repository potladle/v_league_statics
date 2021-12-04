from volleyball.stat.Chance import Chances
from volleyball.stat.StatMaker import *
from volleyball.scraper.LinkProcessor import LinkProcessor
from utills import make_percentage
import statistics
from alive_progress import config_handler

config_handler.set_global(spinner="wait")

score_duration: Dict[int, List[int]] = {}

one_side_score_and_win_percentage : Dict[int, List[int]] = {}

fifth_set_one_side_score_and_win_percentage : Dict[int, List[int]] = {}


def processor_in_set(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: Set):
    index = 0
    left_score_and_duration = [0, 0]
    right_score_and_duration = [0, 0]
    while index < len(rallies):
        if rallies[index].score[0] == left_score_and_duration[0]:
            left_score_and_duration[1] += 1
        elif rallies[index].score[0] != left_score_and_duration[0]:
            if left_score_and_duration[0] in score_duration.keys():
                score_duration[left_score_and_duration[0]].append(left_score_and_duration[1])
            else:
                score_duration[left_score_and_duration[0]] = [left_score_and_duration[1]]
            left_score_and_duration = [rallies[index].score[0], 1]

        if rallies[index].score[1] == right_score_and_duration[0]:
            right_score_and_duration[1] += 1
        elif rallies[index].score[1] != right_score_and_duration[0]:
            if right_score_and_duration[0] in score_duration.keys():
                score_duration[right_score_and_duration[0]].append(right_score_and_duration[1])
            else:
                score_duration[right_score_and_duration[0]] = [right_score_and_duration[1]]
            right_score_and_duration = [rallies[index].score[0], 1]

        index += 1

    if set_in_game.index < 4:
        for rally in rallies:
            if rally.score[0] in one_side_score_and_win_percentage.keys():
                one_side_score_and_win_percentage[rally.score[0]][(lambda last_score: 0 if last_score[0] > last_score[1] else 1)(rallies[len(rallies) - 1].score)] += 1
            else:
                one_side_score_and_win_percentage[rally.score[0]] = (lambda last_score: [1, 0] if last_score[0] > last_score[1] else [0, 1])(rallies[len(rallies) - 1].score)

            if rally.score[1] in one_side_score_and_win_percentage.keys():
                one_side_score_and_win_percentage[rally.score[1]][(lambda last_score: 0 if last_score[1] > last_score[0] else 1)(rallies[len(rallies) - 1].score)] += 1
            else:
                one_side_score_and_win_percentage[rally.score[0]] = (lambda last_score: [1, 0] if last_score[1] > last_score[0] else [0, 1])(rallies[len(rallies) - 1].score)
    else:
        for rally in rallies:
            if rally.score[0] in fifth_set_one_side_score_and_win_percentage.keys():
                fifth_set_one_side_score_and_win_percentage[rally.score[0]][(lambda last_score: 0 if last_score[0] > last_score[1] else 1)(rallies[len(rallies) - 1].score)] += 1
            else:
                fifth_set_one_side_score_and_win_percentage[rally.score[0]] = (lambda last_score: [1, 0] if last_score[0] > last_score[1] else [0, 1])(rallies[len(rallies) - 1].score)

            if rally.score[1] in fifth_set_one_side_score_and_win_percentage.keys():
                fifth_set_one_side_score_and_win_percentage[rally.score[1]][(lambda last_score: 0 if last_score[1] > last_score[0] else 1)(rallies[len(rallies) - 1].score)] += 1
            else:
                fifth_set_one_side_score_and_win_percentage[rally.score[0]] = (lambda last_score: [1, 0] if last_score[1] > last_score[0] else [0, 1])(rallies[len(rallies) - 1].score)


link_processor = LinkProcessor(
    [LinkProcessor.WOMEN],
    [LinkProcessor.REGULAR_SEASON, LinkProcessor.PLAY_OFF, LinkProcessor.SEMI_PLAY_OFF, LinkProcessor.CHAMP]
    , list(range(2018, 2021))
    , list(range(1, 3000)))
link_processor.make_round_number()
stat = Stat(link_processor.links)

stat.fill_games()
stat.fill_sets()
stat.fill_messages()
stat.fill_rallies()
stat.fill_chances()

stat.process_in_set(processor_in_set)

for score, durations in sorted(score_duration.items(), key=lambda item: item[0]):
    print(score, statistics.mean(durations), statistics.median(durations))

print("세트 승률")

for score, win_percentage in sorted(one_side_score_and_win_percentage.items(), key=lambda item: item[0]):
    print(score, f"{make_percentage(win_percentage[0] + win_percentage[1], win_percentage[0] - win_percentage[1])}%")

print("5세트 승률")

for score, win_percentage in sorted(fifth_set_one_side_score_and_win_percentage.items(), key=lambda item: item[0]):
    print(score, f"{make_percentage(win_percentage[0] + win_percentage[1], win_percentage[0] - win_percentage[1])}%")
