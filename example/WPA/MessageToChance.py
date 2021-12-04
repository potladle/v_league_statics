from alive_progress import config_handler
from volleyball.stat.Chance import Chances
from volleyball.stat.StatMaker import *
from variable import action_to_class

config_handler.set_global(spinner="wait")


chance_win_percentage : Dict[tuple, List[int]] = {}


def processor_in_set(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: Set):
    for chance in chances:
        chance_messages = messages[chance.side][chance.message_index[0]: chance.message_index[1] + 1]
        anonymous_messages: List[AnonymousMessage] = []
        for chance_message in chance_messages:
            anonymous_messages.append(AnonymousMessage(action=take_key_by_value(action_to_class, type(chance_message)), success_failure=chance_message.success_failure))
            if tuple(anonymous_messages) in chance_win_percentage.keys():
                chance_win_percentage[tuple(anonymous_messages)][chance.result] += 1
            elif chance.result == Chance.CONTINUE:
                chance_win_percentage[tuple(anonymous_messages)] = [1, 0, 0]
            elif chance.result == Chance.WIM:
                chance_win_percentage[tuple(anonymous_messages)] = [0, 1, 0]
            elif chance.result == Chance.LOSE:
                chance_win_percentage[tuple(anonymous_messages)] = [0, 0, 1]


stat_file = StatFile("C:\\Users\\jsmoo\\OneDrive\\바탕 화면\\배구", ["여자부"], [2021], list(range(1, 300)))
stat_file.fill_games()
stat_file.fill_sets()
stat_file.fill_messages()
stat_file.fill_rallies()
stat_file.fill_chances()

stat_file.process_in_set(processor_in_set)

for chance_anonymous_messages, results in chance_win_percentage.items():
    text = "\n"
    for chance_anonymous_message in chance_anonymous_messages:
        text += f"{chance_anonymous_message.action} "
        if chance_anonymous_message.success_failure == Message.SUCCESS:
            text += "성공 "
        elif chance_anonymous_message.success_failure == Message.FAILURE:
            text += "실패 "
    text += f": {results} {make_percentage(results[Chance.WIM]+results[Chance.LOSE]+results[Chance.CONTINUE], results[Chance.WIM]-results[Chance.LOSE])}%"
    print(text)

