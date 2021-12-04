from typing import List
from volleyball.stat.Game import Game


class Player:

    def __init__(self, name: str, back_num: int, season: int, team: str):
        self.name = name
        self.back_num = back_num
        self.season = season
        self.team = team

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name and self.back_num == other.back_num and self.season == other.season and self.team == other.team
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def make_player_description(self) -> str:
        return f"{self.season}-{self.back_num}.{self.name}({self.team})"


class Message:

    ORDINARY = 0
    SUCCESS = 1
    FAILURE = 2

    NOT_ERROR = 0
    LINE_OVER = 1
    DOUBLE_CONTACT = 2
    CATCH_BALL = 3
    OVER_NET = 4
    FOUR_HIT = 5
    NET_TOUCH = 6
    NET_CAUGHT = 7
    OUT = 8
    ETC_ERROR = 9

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        self.index = index
        self.back_num = back_num
        self.name = name
        self.error_type = 0
        self.success_failure = success_failure

    def is_sub_class(self, types: List[type]) -> bool:
        for objective_type in types:
            if issubclass(type(self), objective_type):
                return True
        return False

    def is_right(self, message_type=0, success_failure=-1):
        if (message_type == 0 or message_type == self.__class__) and (success_failure == -1 or success_failure == self.success_failure):
            return True
        else:
            return False

    def make_description(self):
        return str(type(self)) + " " + str(self.__dict__)

    def make_player(self, game: Game, player_type=Player, *args, **kwargs) -> Player:
        left_roster = list(map((lambda dictionary: list(dictionary.keys())[0]), game.stats[0]))
        return player_type(self.name, self.back_num, game.season, (lambda name: game.teams[0] if name in left_roster else game.teams[1])(self.name), *args, **kwargs)


class NoneMessage(Message):

    def __init__(self, index: int, back_num : int = 0, name : str = "", success_failure : int = 0):
        super(NoneMessage, self).__init__(index, back_num, name, success_failure)


class AnonymousMessage:

    def __init__(self, action: str, success_failure: int):
        self.action = action
        self.success_failure = success_failure

    def __eq__(self, other):
        if isinstance(other, AnonymousMessage):
            return self.action == other.action and self.success_failure == other.success_failure
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
