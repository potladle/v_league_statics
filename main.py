import json
import os
from volleyball.stat.Chance import Chances
from volleyball.stat.StatMaker import *
from volleyball.scraper.LinkProcessor import LinkProcessor
from utills import put_key_and_value_to_dictionary, take_key_by_value
from alive_progress import config_handler

config_handler.set_global(spinner="wait")


def action_to_fault(messages: Messages, action_to_fault_dict: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
    new_action_to_class = action_to_class
    new_action_to_class["범실 아님"] = Message.NOT_ERROR
    for message in messages:
        for action, action_class in action_to_class.items():
            if action_class == type(
                    message) and action in action_to_fault_dict.keys() and message.error_type in action_to_fault_dict[
                action].keys():
                error = list(action_class.keys())[list(action_class.values()).index(message.error_type)]
                action_to_fault_dict[action][error] += 1
            elif action_class == type(
                    message) and action in action_to_fault_dict.keys() and message.error_type not in \
                    action_to_fault_dict[action].keys():
                error = list(action_class.keys())[list(action_class.values()).index(message.error_type)]
                action_to_fault_dict[action][error] = 0
            elif action_class == type(message):
                action_to_fault_dict[action] = {}
    return action_to_fault_dict


except_indices = []


def processor_in_set(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: Set):
    try:
        if game.index not in except_indices:
            season = game.season
            game_num = game.game_num
            set_index = set_in_game.index

            if set_index == 0:
                os.makedirs(
                    f"C:\\Users\\jsmoo\\OneDrive\\바탕 화면\\배구\\여자부\\20{season + 3}-20{season + 4} 시즌\\제 {game_num}경기 ({game.teams[0]},{game.teams[1]})")
                json_file = json.dumps(game.__dict__, indent=4, ensure_ascii=False)
                file = open(
                    f"C:\\Users\\jsmoo\\OneDrive\\바탕 화면\\배구\\여자부\\20{season + 3}-20{season + 4} 시즌\\제 {game_num}경기 ({game.teams[0]},{game.teams[1]})\\game.txt"
                    , "w+"
                    , encoding="UTF-8")
                file.write(json_file)
                file.close()
            os.makedirs(
                f"C:\\Users\\jsmoo\\OneDrive\\바탕 화면\\배구\\여자부\\20{season + 3}-20{season + 4} 시즌\\제 {game_num}경기 ({game.teams[0]},{game.teams[1]})\\{set_index + 1}세트")

            json_file = json.dumps([list(put_key_and_value_to_dictionary(message.__dict__, "action", take_key_by_value(action_to_class, type(message))) for message in messages[0])
                                       , list(put_key_and_value_to_dictionary(message.__dict__, "action", take_key_by_value(action_to_class, type(message))) for message in messages[1])], indent=4, ensure_ascii=False)
            file = open(f"C:\\Users\\jsmoo\\OneDrive\\바탕 화면\\배구\\여자부\\20{season + 3}-20{season + 4} 시즌\\제 {game_num}경기 ({game.teams[0]},{game.teams[1]})\\{set_index + 1}세트\\messages.txt"
                        , "w+"
                        , encoding="UTF-8")
            file.write(json_file)
            file.close()

            json_file = json.dumps(list(chance.__dict__ for chance in chances), indent=4, ensure_ascii=False)
            file = open(
                f"C:\\Users\\jsmoo\\OneDrive\\바탕 화면\\배구\\여자부\\20{season + 3}-20{season + 4} 시즌\\제 {game_num}경기 ({game.teams[0]},{game.teams[1]})\\{set_index + 1}세트\\chances.txt"
                , "w+"
                , encoding="UTF-8")
            file.write(json_file)
            file.close()

            json_file = json.dumps(list(rally.__dict__ for rally in rallies), indent=4, ensure_ascii=False)
            file = open(
                f"C:\\Users\\jsmoo\\OneDrive\\바탕 화면\\배구\\여자부\\20{season + 3}-20{season + 4} 시즌\\제 {game_num}경기 ({game.teams[0]},{game.teams[1]})\\{set_index + 1}세트\\rallies.txt"
                , "w+"
                , encoding="UTF-8")
            file.write(json_file)
            file.close()

            json_file = json.dumps(set_in_game.__dict__, indent=4, ensure_ascii=False)
            file = open(
                f"C:\\Users\\jsmoo\\OneDrive\\바탕 화면\\배구\\여자부\\20{season + 3}-20{season + 4} 시즌\\제 {game_num}경기 ({game.teams[0]},{game.teams[1]})\\{set_index + 1}세트\\set.txt"
                , "w+"
                , encoding="UTF-8")
            file.write(json_file)
            file.close()
    except IndexError:
        except_indices.append(game.index)
        print(game.season, game.game_num, game.teams)


link_processor = LinkProcessor(
    [LinkProcessor.WOMEN],
    [LinkProcessor.REGULAR_SEASON, LinkProcessor.PLAY_OFF, LinkProcessor.SEMI_PLAY_OFF, LinkProcessor.CHAMP]
    , list(range(2020, 2021))
    , list(range(0, 300)))
link_processor.make_round_number()
stat = Stat(link_processor.links)
# "https://www.kovo.co.kr/media/popup_result.asp?season=018&g_part=201&r_round=1&g_num=2"

stat.fill_games()
stat.fill_sets()
stat.fill_messages()
stat.fill_rallies()
stat.fill_chances()

stat.process_in_set(processor_in_set)
