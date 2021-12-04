import os
from typing import Dict
from urllib.request import urlopen
from urllib.error import HTTPError
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from volleyball.stat.Game import Game, make_game
from volleyball.stat.Set import make_set
from volleyball.stat.message import *
from volleyball.stat.Rally import *
from volleyball.stat.make_rallies import make_rallies
from volleyball.stat.make_chances import make_chances
from volleyball.stat.Chance import Chance, Chances
from variable import *
from matplotlib import font_manager, rc
from abc import *
from alive_progress import alive_it
from utills import *
import json
import traceback

font_path = "C:\\Users\\jsmoo\\AppData\\Local\\Microsoft\\Windows\\Fonts\\MARUBuriBetaR.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
plt.rc('xtick', labelsize=7)


class Stat:

    def __init__(self, links: List[str]):
        self.links: List[str] = links
        self.soups: List[BeautifulSoup] = []
        self.games: List[Game] = []
        self.sets: List[List[Set]] = []
        self.messages: List[List[List[Messages]]] = []
        self.rallies: List[List[Rallies]] = []
        self.chances: List[List[List[Chance]]] = []
        print("link to soups")
        for link in alive_it(links, len(links)):
            try:
                html = urlopen(link)
                soup = BeautifulSoup(html, "lxml")
                self.soups.append(soup)
            except HTTPError:
                continue

    def fill_games(self):
        print("fill games")
        for i, soup in alive_it(enumerate(self.soups), len(self.soups)):
            self.games.append(make_game(soup, self.links[i], i))

    def fill_sets(self):
        print("fill sets")
        for i, soup in alive_it(enumerate(self.soups), len(self.soups)):
            try:
                self.sets.append(make_set(self.links[i], soup))
            except IndexError:
                self.games.pop(len(self.sets))
                print("error - StatMaker/fill_sets", i, self.games[i].season, self.games[i].game_num, self.games[i].teams)
                continue

    def fill_messages(self):
        print("fill messages")
        for index, soup in alive_it(enumerate(self.soups), len(self.soups)):
            try:
                self.messages.append(make_message_multiple_set(self.links[index], soup))
            except (IndexError, ValueError) as _:
                self.sets.pop(len(self.messages))
                self.games.pop(len(self.messages))
                print("error - StatMaker/fill_messages", index, self.games[index].season, self.games[index].game_num, self.games[index].teams)
                continue

    def fill_rallies(self):
        print("fill rallies")
        for i, game_for_rally in alive_it(enumerate(self.sets), len(self.sets)):
            self.rallies.append([])
            for k, volleyball_set_for_rally in enumerate(game_for_rally):
                try:
                    self.rallies[i].append(make_rallies(self.messages[i][k], volleyball_set_for_rally))
                except (IndexError, ValueError) as _:
                    print("error - StatMaker/fill_rallies", i, self.games[i].season, self.games[i].game_num, self.games[i].teams)
                    self.sets.pop(i)
                    self.games.pop(i)
                    self.messages.pop(i)
                    continue

    def fill_chances(self):
        print("fill chances")
        for i, game_for_rally in alive_it(enumerate(self.sets), len(self.sets)):
            self.chances.append([])
            for k, volleyball_set_for_rally in enumerate(game_for_rally):
                try:
                    self.chances[i].append(make_chances(self.messages[i][k], self.rallies[i][k]))
                except IndexError:
                    print("error - StatMaker/fill_chances", i, self.games[i].season, self.games[i].game_num, self.games[i].teams)
                    print(len(self.chances), len(self.messages), len(self.rallies), i, len(self.messages[i]), len(self.rallies[i]), k)
                    self.sets.pop(i)
                    self.games.pop(i)
                    self.messages.pop(i)
                    self.rallies.pop(i)
                    continue

    def process_in_set(self, method, *args):
        print("process_in_set")
        for game in alive_it(self.games, len(self.games)):
            i = 0
            while True:
                try:
                    for set_in_game in self.sets[game.index - i]:
                        method(self.messages[game.index - i][set_in_game.index], self.chances[game.index - i][set_in_game.index], self.rallies[game.index - i][set_in_game.index], game, set_in_game, *args)
                    break
                except IndexError:
                    i += 1


class StatFile:
    def __init__(self
                 , folder_path: str
                 , gender: List[str]
                 , season: List[int]
                 , game_num: List[int]):
        self.folder_path: str = folder_path
        self.folder_paths: List[str] = []

        if "낭자부" in gender:
            season_path = map(lambda one_season: folder_path + "\\남자부" + f"\\{one_season - 1}-{one_season} 시즌", season)
            for one_season_path in season_path:
                game_folder = os.scandir(one_season_path)
                for one_game_folder in game_folder:
                    if one_game_folder in game_num:
                        self.folder_paths.append(one_season_path + str(one_game_folder))

        if "여자부" in gender:
            season_path = map(lambda one_season: folder_path + "\\여자부" + f"\\{one_season - 1}-{one_season} 시즌", season)
            for one_season_path in season_path:
                game_folder = os.scandir(one_season_path)
                for one_game_folder in game_folder:
                    if extract_first_digit(str(one_game_folder)) in game_num:
                        self.folder_paths.append(one_season_path + "\\" + one_game_folder.name)

        self.games: List[Game] = []
        self.sets: List[List[Set]] = []
        self.messages: List[List[List[Messages]]] = []
        self.rallies: List[List[Rallies]] = []
        self.chances: List[List[Chances]] = []

    def fill_games(self):
        for one_game_folder in self.folder_paths:
            with open(one_game_folder + "\\game.txt", encoding="UTF-8") as game_file:
                game_json = json.load(game_file)
                existing_game = Game(**game_json)
                existing_game.index = len(self.games)
                self.games.append(existing_game)

    def fill_sets(self):
        for i, one_game_folder in enumerate(self.folder_paths):
            self.sets.append([])
            set_folders = os.scandir(one_game_folder)
            for v, _ in enumerate(list(set_folders)[:-1]):
                with open(one_game_folder + f"\\{v + 1}세트\\set.txt", encoding="UTF-8") as file:
                    set_json = json.load(file)
                    self.sets[i].append(Set(**set_json))

    def fill_messages(self):
        for t, one_game_folder in enumerate(self.folder_paths):
            self.messages.append([])
            set_folders = os.scandir(one_game_folder)
            for v, _ in enumerate(list(set_folders)[:-1]):
                with open(one_game_folder + f"\\{v + 1}세트\\messages.txt", encoding="UTF-8") as file:
                    messages_json = json.load(file)
                    two_messages: List[Messages] = [Messages([]), Messages([])]
                    for i, messages in enumerate(messages_json):
                        for one_message_json in messages:
                            if one_message_json["action"] == "팀득점" or one_message_json["action"] == "팀실패":
                                two_messages[i].append(TeamMessage(one_message_json["index"], one_message_json["success_failure"]))
                            else:
                                two_messages[i].append(action_to_class[one_message_json["action"]](**remove_key(remove_key(one_message_json, "action"), "error_type")))
                                two_messages[i][last_index(two_messages[i])].error_type = one_message_json["error_type"]

                    self.messages[t].append(two_messages)

    def fill_chances(self):
        for t, one_game_folder in enumerate(self.folder_paths):
            self.chances.append([])
            set_folders = os.scandir(one_game_folder)
            for i, _ in enumerate(list(set_folders)[:-1]):
                with open(one_game_folder + f"\\{i + 1}세트\\chances.txt", encoding="UTF-8") as file:
                    chances_json = json.load(file)
                    chances: List[Chance] = []
                    for chance in chances_json:
                        chances.append(Chance(**chance))
                    self.chances[t].append(Chances(chances))

    def fill_rallies(self):
        for t, one_game_folder in enumerate(self.folder_paths):
            self.rallies.append([])
            set_folders = os.scandir(one_game_folder)
            for i, _ in enumerate(list(set_folders)[:-1]):
                with open(one_game_folder + f"\\{i + 1}세트\\rallies.txt", encoding="UTF-8") as file:
                    rallies_json = json.load(file)
                    rallies: Rallies = Rallies([])
                    for rally in rallies_json:
                        rallies.append(Rally(**rally))
                    self.rallies[t].append(rallies)

    def process_in_set(self, method, *args):
        print("process_in_set")
        for game in alive_it(self.games, len(self.games)):
            i = 0
            while True:
                try:
                    for set_in_game in self.sets[game.index - i]:
                        method(self.messages[game.index - i][set_in_game.index], self.chances[game.index - i][set_in_game.index], self.rallies[game.index - i][set_in_game.index], game, set_in_game, *args)
                    break
                except IndexError:
                    print(f"error {i}")
                    print(traceback.format_exc())
                    i += 1


class ShareCalc(Dict[Player, int]):

    def __init__(self, dictionary: Dict[Player, int]):
        super(ShareCalc, self).__init__(dictionary)

    def make_action_and_time(self, messages: Messages, game: Game, action_type: str):
        for action_message in messages:
            if isinstance(action_message, action_to_class[action_type]):
                if action_message.make_player(game) not in self.keys():
                    self[action_message.make_player(game)] = 1
                else:
                    self[action_message.make_player(game)] += 1

    def sort_share(self):
        sorted_tuples = sorted(self.items(), key=lambda item: item[1], reverse=True)
        return self.__class__({k: v for k, v in sorted_tuples})

    def print_share(self, name: str = "", limit: int = 0) -> str:
        if limit == 0:
            limit = len(self)
        whole = 0
        for value in self.values():
            whole += value

        index = 0
        string = name + "\n"
        for player, time in self.items():
            string += f"{player.season}-{player.back_num}.{player.name}({player.team}): {int(time/whole * 1000)/10}% {time}/{whole} \n"
            index += 1
            if index == limit:
                break
        return string

    def make_share_graph(self, fig, title: str, position: int, limit: int = 0, reverse: bool = True):
        if limit == 0:
            limit = len(self)
        whole = 0
        for trial in self.values():
            whole += trial
        sorted_tuples = sorted(self.items(), key=lambda item: item[1], reverse=reverse)[:limit]
        x = [player.name for player, trial in sorted_tuples]
        y = [trial / whole for player, trial in sorted_tuples]
        ax = fig.add_subplot(position)
        ax.set_title(title)
        ax.set_ylim([0, 0.6])
        ax.plot(x, y, 'go')

    def comparing_share_graph(self, others, fig, legends: List[str], title: str, position: int, limit: int = 0, reverse: bool = True):
        """이 점유율 기준 상위 limit 명 대상 비교"""
        if limit == 0:
            limit = len(self)
        whole = 0
        for trial in self.values():
            whole += trial
        sorted_tuples = sorted(self.items(), key=lambda item: item[1], reverse=reverse)[:limit]
        players = [player for player, trial in sorted_tuples]
        x = [player.name for player in players]
        y = [trial / whole for player, trial in sorted_tuples]
        y_ax = [y]

        for other in others:
            other_whole = 0
            for trial in other.values():
                other_whole += trial

            y = []
            for player in players:
                y.append(other[player]/other_whole)
            y_ax.append(y)
        ax = fig.add_subplot(position)
        ax.set_title(title)
        ax.set_ylim([0, 0.6])
        for i, y in enumerate(y_ax):
            ax.plot(x, y, color[i], label=legends[i])
        plt.legend(fontsize=5)


class EffCalc(Dict[Player, List[int]]):
    """플레이어 : [시도, 성공, 실패(상대 블로킹 성공)]"""

    def __init__(self, dictionary):
        super(EffCalc, self).__init__(dictionary)

    def find_stat_with_name(self, name):
        try:
            index = list(map(lambda player: player.name, self.keys())).index(name)
            return list(self.items())[index][1]
        except ValueError:
            return [0, 0, 0]

    def append_directly(self, game: Game, message: Message, player_type, *args, **kwargs):
        player = message.make_player(game, player_type, *args, **kwargs)
        if player in self.keys():
            self[player][message.success_failure] += 1
            if message.success_failure != 0:
                self[player][0] += 1
        else:
            self[player] = [0, 0, 0]
            self[player][message.success_failure] += 1
            if message.success_failure != 0:
                self[player][0] += 1

    def append_effect_calc(self, messages: Messages, game: Game, action_type: str, player_type=Player, *args, **kwargs):
        action_messages = list(filter(lambda message: isinstance(message, action_to_class[action_type]), messages))
        for action_message in action_messages:
            action_message: Message
            self.append_directly(game, action_message, player_type, *args, **kwargs)

    def return_whole_trial(self):
        whole_trial = 0
        for value in self.values():
            whole_trial += value[0]
        return whole_trial

    def print_effect_with_name(self, make_distinct: bool = True, print_or_not: bool = True, prefix: str = "", top_n: int = 5, at_least: int = 0):
        last_string = prefix
        sorted_tuples = sorted(self.items(), key=lambda item: item[1], reverse=True)[:top_n]
        for player, numbers in sorted_tuples:
            if numbers[0] >= at_least:
                last_string += f"\n{player.make_player_description()}: {int(int((numbers[1] - numbers[2])/numbers[0] * 1000)/10)}% {numbers[0]}/{numbers[1]}/{numbers[2]}"
        if make_distinct:
            last_string += "\n" + "-" * 100
        if print_or_not:
            print(last_string)
        return last_string

    def print_trial_with_name(self, make_distinct: bool = True, print_or_not: bool = True, at_least: int = 0):
        last_string = ""
        for player, numbers in self.items():
            if numbers[0] >= at_least:
                last_string += f"\n{player.make_player_description()}: {numbers[0]}"
        if make_distinct:
            last_string += "\n" + "-" * 100
        if print_or_not:
            print(last_string)

    def print_overall_effect(self, print_or_not: bool = True, prefix: str = ""):
        overall_trial = 0
        overall_succession = 0
        overall_failure = 0
        for numbers in self.values():
            overall_trial += numbers[0]
            overall_succession += numbers[1]
            overall_failure += numbers[2]

        prefix += f" {int(int((overall_succession - overall_failure)/overall_trial * 1000)/10)}% {overall_trial}/{overall_succession}/{overall_failure}"

        if print_or_not:
            print(prefix)

        return prefix

    def print_overall_trial(self, print_or_not: bool = True, prefix : str = ""):
        overall_trial = 0
        for numbers in self.values():
            overall_trial += numbers[0]

        prefix += f" {overall_trial}"

        if print_or_not:
            print(prefix)

        return prefix

    def print_multiple_eff_calc(self, overall: bool, eff_calculators: List, eff_formula, print_or_not: bool = True, prefix="", top_n: int = 5):
        for eff_calculator in eff_calculators:
            for player, stat in self.items():
                try:
                    self[player].append(eff_calculator[player][0])
                except KeyError:
                    self[player].append(0)

        if overall:
            overall = []
            first_stat = list(self.values())[0]
            for i, _ in enumerate(first_stat):
                for value in self.values():
                    if len(overall) == i:
                        overall.append(value[i])
                    else:
                        overall[i] += value[i]
            if print_or_not:
                print(overall)
                return str(overall)
            else:
                return str(overall)
        else:
            text = prefix
            sorted_tuples = sorted(self.items(), key=lambda item: item[1], reverse=True)[:top_n]
            for player, stat in sorted_tuples:
                text += f"\n{player.make_player_description()}: " + eff_formula(stat, player)

            if print_or_not:
                print(text)
                return text
            else:
                return text


class CollectorItem(metaclass=ABCMeta):

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __members(self):
        return self.key, self.value

    def __eq__(self, other):
        if type(self) == type(other):
            return self.__members() == other.__members()
        else:
            return False

    def __hash__(self):
        return hash(self.__members())

    @abstractmethod
    def make_description(self) -> str:
        pass

    @abstractmethod
    def collector_append_directly(self, collector_item, collector):
        """collector 를 직접 변경 시키는 방식으로 진행"""
        pass

    @abstractmethod
    def find_by_key(self, *args, **kwargs) -> bool:
        pass


class Collector(list):

    def __init__(self):
        super(Collector, self).__init__([])

    def append_to_collector(self, collector_item: CollectorItem):
        collector_item.collector_append_directly(collector_item, self)

    def print_collection(self, distinction_or_not: bool, print_or_not: bool):
        final = ""
        for collector_item in self:
            final = final + "\n" + collector_item.make_description()

        if print_or_not:
            print(final)
        if distinction_or_not:
            print("\n" + "-" * 100)

    def find_collector_item(self, *args, **kwargs):
        for collector_item in self:
            if collector_item.find_by_key(*args, **kwargs):
                return collector_item
        raise ValueError
