from volleyball.stat.StatMaker import *
from typing import List
from openpyxl import Workbook

stat_file = StatFile("C:\\Users\\jsmoo\\OneDrive\\바탕 화면\\배구", ["여자부"], [2021], list(range(1, 300)))
stat_file.fill_games()
stat_file.fill_sets()
stat_file.fill_messages()
stat_file.fill_rallies()
stat_file.fill_chances()

home_team_receives : Dict[str, EffCalc] = {}

away_team_receives : Dict[str, EffCalc] = {}

home_team_serves : Dict[str, EffCalc] = {}

away_team_serves : Dict[str, EffCalc] = {}

home_team_attacks : Dict[str, EffCalc] = {}

away_team_attacks : Dict[str, EffCalc] = {}


class PlayerWithSetNum(Player):

    def __init__(self, set_num: int, name: str, back_num: int, season: int, team: str):
        super().__init__(name, back_num, season, team)
        self.set_num = set_num


def put_action_message_to_action(messages: List[Messages], game: Game, set_in_game: Set, action: str, home_eff_calc: Dict[str, EffCalc], away_eff_calc: Dict[str, EffCalc]):
    for message in messages[0].select_messages_with_action(action):
        home_team = game.teams[0]
        if home_team not in list(home_eff_calc.keys()):
            home_eff_calc[home_team] = EffCalc({})
            home_eff_calc[home_team].append_effect_calc(Messages([message]), game, action, PlayerWithSetNum, set_in_game.index + 1)
        else:
            home_eff_calc[home_team].append_effect_calc(Messages([message]), game, action, PlayerWithSetNum, set_in_game.index + 1)

    for message in messages[1].select_messages_with_action(action):
        home_team = game.teams[0]
        if home_team not in list(away_eff_calc.keys()):
            away_eff_calc[home_team] = EffCalc({})
            away_eff_calc[home_team].append_effect_calc(Messages([message]), game, action, PlayerWithSetNum, set_in_game.index + 1)
        else:
            away_eff_calc[home_team].append_effect_calc(Messages([message]), game, action, PlayerWithSetNum, set_in_game.index + 1)


def processor_in_set(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: Set):
    for rally in rallies:
        chances_in_rally = []
        for index in range(rally.message_index[0], rally.message_index[1] + 1):
            chance = chances.select_chance_with_message_index(index)
            if chance not in chances_in_rally:
                chances_in_rally.append(chance)

    actions_home_away = [
        ["리시브", home_team_receives, away_team_receives],
        ["서브", home_team_serves, away_team_serves],
        ["공격종합", home_team_attacks, away_team_attacks]
    ]

    for action_home_away in actions_home_away:
        put_action_message_to_action(messages, game, set_in_game, action_home_away[0], action_home_away[1], action_home_away[2])


stat_file.process_in_set(processor_in_set)


for team, eff_calc in list(home_team_serves.items()):
    eff_calc: EffCalc
    eff_calc.print_overall_effect(prefix=team + " 서브")

print("-" * 50)

for team, eff_calc in list(away_team_serves.items()):
    eff_calc: EffCalc
    eff_calc.print_overall_effect(prefix=team + " 서브")

print("-" * 50)

for team, eff_calc in list(home_team_receives.items()):
    eff_calc: EffCalc
    eff_calc.print_overall_effect(prefix=team + " 리시브")

print("-" * 50)

for team, eff_calc in list(away_team_receives.items()):
    eff_calc: EffCalc
    eff_calc.print_overall_effect(prefix=team + " 리시브")

print("-" * 50)

for team, eff_calc in list(home_team_attacks.items()):
    eff_calc: EffCalc
    eff_calc.print_overall_effect(prefix=team + " 공격")

print("-" * 50)

for team, eff_calc in list(away_team_receives.items()):
    eff_calc: EffCalc
    eff_calc.print_overall_effect(prefix=team + " 공격")
