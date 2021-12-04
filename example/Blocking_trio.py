from volleyball.stat.Chance import Chances
from volleyball.stat.StatMaker import *
from volleyball.scraper.LinkProcessor import LinkProcessor
from utills import make_percentage
from copy import deepcopy

link_processor = LinkProcessor(
    [LinkProcessor.WOMEN],
    [LinkProcessor.REGULAR_SEASON, LinkProcessor.PLAY_OFF, LinkProcessor.SEMI_PLAY_OFF, LinkProcessor.CHAMP]
    , list(range(2020, 2021))
    , list(range(1, 3000)))
link_processor.make_round_number()
stat = Stat(link_processor.links)

stat.fill_games()
stat.fill_sets()
stat.fill_messages()
stat.fill_rallies()
stat.fill_chances()


def fill_effects_women_teams(effects: Dict[str, EffCalc]):
    for women_team in women_teams:
        effects[women_team] = EffCalc({})


blocking_trio_effects: Dict[str, EffCalc] = {}
fill_effects_women_teams(blocking_trio_effects)

effective_blocking_trio_effects: Dict[str, EffCalc] = {}
fill_effects_women_teams(effective_blocking_trio_effects)

blocking_assist_trio_effects: Dict[str, EffCalc] = {}
fill_effects_women_teams(blocking_assist_trio_effects)

blocking_effects: EffCalc = EffCalc({})

effective_blocking_effects: EffCalc = EffCalc({})

blocking_assist_effects: EffCalc = EffCalc({})


class TrioPlayer(Player):
    def __init__(self, name: str, back_num: int, season: int, team: str, names: List[str]):
        super(TrioPlayer, self).__init__(str(names)[1:-1], 0, season, team)
        self.names = tuple(names)

    def make_player_description(self) -> str:
        return f"{self.season}-{self.name}({self.team})"


def processor_in_set(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: Set):
    for rally in rallies:
        front = rally.rotation[0][1:4]
        messages_in_rally = messages[0].slice_messages_with_rallies(Rallies([rally]))
        blocking_trio_effects[game.teams[0]].append_effect_calc(messages_in_rally, game, "블로킹", TrioPlayer, front)
        blocking_assist_trio_effects[game.teams[0]].append_effect_calc(messages_in_rally, game, "블로킹어시스트", TrioPlayer, front)
        effective_blocking_trio_effects[game.teams[0]].append_effect_calc(messages_in_rally, game, "유효블로킹", TrioPlayer, front)

        front = rally.rotation[1][1:4]
        messages_in_rally = messages[1].slice_messages_with_rallies(Rallies([rally]))
        blocking_trio_effects[game.teams[1]].append_effect_calc(messages_in_rally, game, "블로킹", TrioPlayer, front)
        blocking_assist_trio_effects[game.teams[1]].append_effect_calc(messages_in_rally, game, "블로킹어시스트", TrioPlayer, front)
        effective_blocking_trio_effects[game.teams[1]].append_effect_calc(messages_in_rally, game, "유효블로킹", TrioPlayer, front)

    blocking_effects.append_effect_calc(messages[0], game, "블로킹")
    blocking_assist_effects.append_effect_calc(messages[0], game, "블로킹어시스트")
    effective_blocking_effects.append_effect_calc(messages[0], game, "유효블로킹")

    blocking_effects.append_effect_calc(messages[1], game, "블로킹")
    blocking_assist_effects.append_effect_calc(messages[1], game, "블로킹어시스트")
    effective_blocking_effects.append_effect_calc(messages[1], game, "유효블로킹")


stat.process_in_set(processor_in_set)


def effect_formula(effect_stat, player):
    blocking_stats : List[List[int]] = []
    for player_name in player.names:
        gross_blocking_effect = deepcopy(blocking_effects.find_stat_with_name(player_name))
        gross_blocking_effect.append(blocking_assist_effects.find_stat_with_name(player_name)[0])
        gross_blocking_effect.append(effective_blocking_effects.find_stat_with_name(player_name)[0])
        blocking_stats.append(gross_blocking_effect)

    blocking_gross_stat: List[int] = [0, 0, 0, 0, 0]

    for blocking_stat in blocking_stats:
        for i, one_blocking_stat in enumerate(blocking_stat):
            blocking_gross_stat[i] += one_blocking_stat

    return f"{effect_stat[0]}/{effect_stat[1]}/{effect_stat[2]}/{effect_stat[3]}/{effect_stat[4]}" \
           f" {make_percentage(effect_stat[1], effect_stat[3])}% {effect_stat[3]}/{effect_stat[1]}" \
           f" {make_percentage(blocking_gross_stat[1], effect_stat[1])}% {effect_stat[1]}/{blocking_gross_stat[1]}" \
           f" {make_percentage(blocking_gross_stat[3], effect_stat[3])}% {effect_stat[3]}/{blocking_gross_stat[3]}" \
           f" {make_percentage(blocking_gross_stat[4], effect_stat[4])}% {effect_stat[4]}/{blocking_gross_stat[4]}"


for object_team, blocking_trio_effect in blocking_trio_effects.items():
    blocking_trio_effect.print_effect_with_name(prefix=object_team)

for object_team, blocking_trio_effect in blocking_assist_trio_effects.items():
    blocking_trio_effect.print_effect_with_name(prefix=object_team)

for object_team, blocking_trio_effect in effective_blocking_trio_effects.items():
    blocking_trio_effect.print_effect_with_name(prefix=object_team)

for object_team, blocking_trio_effect in blocking_trio_effects.items():
    blocking_trio_effect.print_multiple_eff_calc(False, [blocking_assist_trio_effects[object_team], effective_blocking_trio_effects[object_team]], effect_formula, prefix=object_team)
