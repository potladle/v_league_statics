import pandas
from volleyball.stat.Chance import Chances
from volleyball.stat.StatMaker import *
from volleyball.scraper.LinkProcessor import LinkProcessor
from utills import take_key_by_value

stat_file = StatFile("C:\\Users\\jsmoo\\OneDrive\\바탕 화면\\배구", ["여자부"], [2021], list(range(1, 300)))
stat_file.fill_games()
stat_file.fill_sets()
stat_file.fill_messages()
stat_file.fill_rallies()
stat_file.fill_chances()


class RallyResultEffectCollectorItem(CollectorItem):

    def __init__(self, messages: Messages, rally_result: int):
        new_key = tuple(
                   (map
                    (lambda object_message: frozenset({take_key_by_value(action_to_class, type(object_message))
                                                       : object_message.success_failure}.items()),
                     messages)))
        new_value = [0, 0]
        if rally_result == 1:
            new_value[0] += 1
        elif rally_result == -1:
            new_value[1] += 1
        self.win_percentage = (new_value[0] - new_value[1])/(new_value[0] + new_value[1])
        super().__init__(new_key, new_value)

    def make_description(self) -> str:
        description = ""
        for action_result in list(self.key):
            action_result: Dict[str, int] = dict(action_result)
            description += list(action_result.keys())[0]
            if list(action_result.values())[0] == Message.SUCCESS:
                description += " 성공 "
            elif list(action_result.values())[0] == Message.FAILURE:
                description += " 실패 "
            else:
                description += " "
        description += f" : "
        description += f"{self.value}"
        return description

    def collector_append_directly(self, collector_item, collector):
        if collector_item.key in list(map(lambda one_collector_item: one_collector_item.key, collector)):
            index = list(map(lambda one_collector_item: one_collector_item.key, collector)).index(collector_item.key)
            if collector_item.value[0] == 1:
                collector[index].value[0] += 1
            elif collector_item.value[1] == 1:
                collector[index].value[1] += 1
            collector_item.win_percentage = (collector_item.value[0] - collector_item.value[1])/(collector_item.value[0] + collector_item.value[1])
        else:
            collector.append(collector_item)

    def find_by_key(self, *args, **kwargs) -> bool:
        new_key = tuple(
                   (map
                    (lambda object_message: frozenset({take_key_by_value(action_to_class, type(
                        object_message)): object_message.success_failure}.items()),
                     args[0])))
        return new_key == self.key


effect_with_rally_collector = Collector()

player_to_win_percentage: Dict[Player, int] = {}


def processor_in_set_1(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: Set):
    print(game.index, set_in_game.index, "1")
    for message in messages[0]:
        if not isinstance(message, EtcMessage) and not isinstance(messages[1][message.index], EtcMessage) \
                and not isinstance(message, SubstituteMessage) and not isinstance(messages[1][message.index],
                                                                                  SubstituteMessage) \
                and not isinstance(message, TeamMessage) and not isinstance(messages[1][message.index], TeamMessage) \
                and not isinstance(message, NoneMessage):
            rally = rallies.select_rally_inner_message_index(message.index)
            mapped_messages = Messages(list(map(
                lambda one_message: one_message
                if type(one_message) is not NoneMessage
                else messages[1][one_message.index]
                , messages[0][rally.message_index[0]: message.index + 1])))
            collector_item = RallyResultEffectCollectorItem(mapped_messages
                                                            , (lambda winner: 1 if winner == 0 else -1)(rally.winner))
            effect_with_rally_collector.append_to_collector(collector_item)
    for message in messages[1]:
        if not issubclass(type(message), EtcMessage) and not issubclass(type(messages[0][message.index]), EtcMessage) \
                and not isinstance(message, SubstituteMessage) and not isinstance(messages[0][message.index],
                                                                                  SubstituteMessage) \
                and not isinstance(message, TeamMessage) and not isinstance(messages[0][message.index], TeamMessage) \
                and not isinstance(message, NoneMessage):
            rally = rallies.select_rally_inner_message_index(message.index)
            mapped_messages = Messages(list(map(
                lambda one_message: one_message
                if type(one_message) is not NoneMessage
                else messages[0][one_message.index]
                , messages[1][rally.message_index[0]: message.index + 1])))
            collector_item = RallyResultEffectCollectorItem(mapped_messages
                                                            , (lambda winner: -1 if winner == 0 else 1)(rally.winner))
            effect_with_rally_collector.append_to_collector(collector_item)


def processor_in_set_2(messages: List[Messages], chances: Chances, rallies: Rallies, game: Game, set_in_game: Set):
    print(game.index, set_in_game.index, "2")
    for message in messages[0]:
        if type(message) != TeamMessage and not isinstance(message, SubstituteMessage) and not isinstance(message, EtcMessage) \
                and type(messages[1][message.index]) != TeamMessage \
                and not isinstance(messages[1][message.index], SubstituteMessage) \
                and not isinstance(messages[1][message.index], EtcMessage) \
                and not isinstance(message, NoneMessage):
            rally = rallies.select_rally_inner_message_index(message.index)
            mapped_messages = Messages(list(map(
                    lambda one_message: one_message
                    if type(one_message) is not NoneMessage
                    else messages[1][one_message.index]
                    , messages[0][rally.message_index[0]: message.index + 1])))

            if message.make_player(game) in list(player_to_win_percentage.keys()):
                if isinstance(message, ServeMessage):
                    collector_item = effect_with_rally_collector.find_collector_item(mapped_messages)
                    player_to_win_percentage[message.make_player(game)] += collector_item.win_percentage
                else:
                    collector_item = effect_with_rally_collector.find_collector_item(mapped_messages)
                    now_win_percentage = collector_item.win_percentage

                    previous_mapped_messages = mapped_messages[:-1]
                    previous_collector_item = effect_with_rally_collector.find_collector_item(previous_mapped_messages)
                    previous_win_percentage = previous_collector_item.win_percentage

                    if type(messages[0][message.index - 1]) == NoneMessage:
                        player_to_win_percentage[
                            message.make_player(game)] += now_win_percentage + previous_win_percentage
                    else:
                        player_to_win_percentage[
                            message.make_player(game)] += now_win_percentage - previous_win_percentage
            else:
                collector_item = effect_with_rally_collector.find_collector_item(mapped_messages)
                player_to_win_percentage[message.make_player(game)] = collector_item.win_percentage

    for message in messages[1]:
        if type(message) != TeamMessage and not isinstance(message, SubstituteMessage) and not isinstance(message, EtcMessage)\
            and type(messages[0][message.index]) != TeamMessage\
            and not isinstance(messages[0][message.index], SubstituteMessage)\
            and not isinstance(messages[0][message.index], EtcMessage)\
            and not isinstance(message, NoneMessage):
            rally = rallies.select_rally_inner_message_index(message.index)
            mapped_messages = Messages(list(map(
                        lambda one_message: one_message
                        if type(one_message) is not NoneMessage
                        else messages[0][one_message.index]
                        , messages[1][rally.message_index[0]: message.index + 1])))

            if message.make_player(game) in list(player_to_win_percentage.keys()):
                if isinstance(message, ServeMessage):
                    collector_item = effect_with_rally_collector.find_collector_item(mapped_messages)
                    player_to_win_percentage[message.make_player(game)] += collector_item.win_percentage
                else:
                    collector_item = effect_with_rally_collector.find_collector_item(mapped_messages)
                    now_win_percentage = collector_item.win_percentage

                    previous_mapped_messages = mapped_messages[:-1]
                    previous_collector_item = effect_with_rally_collector.find_collector_item(previous_mapped_messages)
                    previous_win_percentage = previous_collector_item.win_percentage

                    if type(messages[1][message.index - 1]) == NoneMessage:
                        player_to_win_percentage[message.make_player(game)] += now_win_percentage + previous_win_percentage
                    else:
                        player_to_win_percentage[message.make_player(game)] += now_win_percentage - previous_win_percentage
            else:
                collector_item = effect_with_rally_collector.find_collector_item(mapped_messages)
                player_to_win_percentage[message.make_player(game)] = collector_item.win_percentage


stat_file.process_in_set(processor_in_set_1)

effect_with_rally_collector.print_collection(distinction_or_not=False, print_or_not=True)

df = pandas.DataFrame(map(lambda collector_item: {collector_item.key: collector_item.value}, effect_with_rally_collector))
print(df.head())

stat_file.process_in_set(processor_in_set_2)

for key, value in player_to_win_percentage.items():
    print(key.__dict__, value)
