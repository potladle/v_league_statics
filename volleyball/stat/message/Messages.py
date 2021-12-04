from volleyball.stat.message.Message import *
from variable import *
from collections import Counter
from typing import List
from volleyball.stat.Game import Game
from volleyball.stat.Rally import Rally, Rallies


class Messages(List[Message]):

    def __init__(self, messages: List[Message]):
        super(Messages, self).__init__(messages)

    def __sub__(self, other):
        return self.__class__([item for item in self if item not in other])

    def find_main_player(self, action: str, game: Game) -> Player:
        players = []
        for message in self:
            if message.is_sub_class([action_to_class[action]]):
                players.append(message.make_player(game))

        return Counter(players).most_common(1)[0][0]

    def select_messages_with_action(self, action: str):
        new_messages: List[action_to_class[action]] = []
        for message in self:
            if message.is_sub_class([action_to_class[action]]):
                new_messages.append(message)

        return self.__class__(new_messages)

    def select_messages_with_action_and_result(self, action: str, result: int):
        new_messages: List[action_to_class[action]] = []
        for message in self:
            if message.is_sub_class([action_to_class[action]]) and message.success_failure == result:
                new_messages.append(message)

        return self.__class__(new_messages)

    def select_messages_with_player(self, player, game: Game):
        new_messages = []
        if isinstance(player, Player):
            for message in self:
                if player == message.make_player(game):
                    new_messages.append(message)
        elif isinstance(player, List):
            for message in self:
                if message.make_player(game) in player:
                    new_messages.append(message)
        else:
            raise TypeError("플레이어를 확인해 주세요")
        return self.__class__(new_messages)

    def select_messages_with_player_and_action(self, player, action: str, game: Game):
        new_messages: List[action_to_class[action]] = []
        if isinstance(player, Player):
            for message in self:
                if message.is_sub_class([action_to_class[action]]) and player == message.make_player(game):
                    new_messages.append(message)
        elif isinstance(player, List):
            for message in self:
                if message.is_sub_class([action_to_class[action]]) and message.make_player(game) in player:
                    new_messages.append(message)
        else:
            raise TypeError("플레이어를 확인해 주세요")
        return self.__class__(new_messages)

    def select_messages_with_player_name_and_action(self, player_name, action: str, game: Game):
        new_messages: List[action_to_class[action]] = []
        if isinstance(player_name, str):
            for message in self:
                if message.is_sub_class([action_to_class[action]]) and player_name == message.make_player(game).name:
                    new_messages.append(message)
        elif isinstance(player_name, List):
            for message in self:
                if message.is_sub_class([action_to_class[action]]) and message.make_player(game).name in player_name:
                    new_messages.append(message)
        else:
            raise TypeError("플레이어를 확인해 주세요")
        return self.__class__(new_messages)

    def select_messages_with_player_name(self, player_name, game: Game):
        new_messages: List[Message] = []
        if isinstance(player_name, str):
            for message in self:
                if player_name == message.make_player(game).name:
                    new_messages.append(message)
        elif isinstance(player_name, List):
            for message in self:
                if message.make_player(game).name in player_name:
                    new_messages.append(message)
        else:
            raise TypeError("플레이어를 확인해 주세요")
        return self.__class__(new_messages)

    def select_attack_messages_after_set(self, set_messages: List[Message]):
        attacks: List[Message] = []
        for set_message in set_messages:
            set_message: SetMessage
            attack_message = set_message.find_next_message(self)
            if isinstance(attack_message, AttackMessage):
                attacks.append(attack_message)
        return self.__class__(attacks)

    def select_set_messages_after_receive(self, receive_messages: List[ReceiveMessage]):
        sets: List[Message] = []
        for receive_message in receive_messages:
            set_message = receive_message.find_next_message(self)
            if isinstance(set_message, SetMessage):
                sets.append(set_message)
        return self.__class__(sets)

    def slice_messages_with_rallies(self, rallies: List[Rally]):
        if len(rallies) != 0:
            new_messages = self.__class__([])
            for rally in rallies:
                new_messages += self[rally.message_index[0]: rally.message_index[1] + 1]
            return new_messages
        else:
            return self.__class__([])

    def slice_messages_with_chance(self, chance):
        # chance: Chance
        return self[chance.message_index[0]: chance.message_index[1] + 1]

    def select_messages_after_put(self, rallies: Rallies, game: Game, size=1):
        new_messages = []
        putting_messages = self.select_messages_with_action("투입")
        for putting_message in putting_messages:
            new_rallies = rallies.select_rally_after_message_index(putting_message.index, size)
            new_messages += self.slice_messages_with_rallies(new_rallies).select_messages_with_player(
                putting_message.make_player(game), game)
        return new_messages
