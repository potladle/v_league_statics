from volleyball.stat.message.AttackMessage import *
from volleyball.stat.message.DefenseMessage import *


class Chance:
    LEFT = 0
    RIGHT = 1

    CONTINUE = 0
    WIM = 1
    LOSE = 2

    def __init__(self, side: int, result: int, message_index: List[int], index: int):
        self.side = side
        self.result = result
        self.message_index = message_index
        self.index = index

    def other_side(self) -> int:
        if self.side == 0:
            return 1
        else:
            return 0


class Chances(List[Chance]):

    def __init__(self, chances: List[Chance]):
        super(Chances, self).__init__(chances)

    """for index, chance in enumerate(chances):
        if index == len(chances) - 1:
            break
        if chance.message_index[0] == chance.message_index[1] \
            and isinstance(messages[chance.side][chance.message_index[0]], ReceiveMessage) \
            and isinstance(messages[chance.other_side()][chances[index + 1].message_index[0]], AttackMessage):
            direct_effect.append_effect_calc(
                Messages([messages[chance.other_side()][chances[index + 1].message_index[0]]]), game, "공격종합")

    for index, chance in enumerate(chances):
        if index == len(chances) - 1:
            break
        if chance.message_index[0] == chance.message_index[1] \
            and isinstance(messages[chance.side][chance.message_index[0]], ReceiveMessage) \
            and isinstance(messages[chance.other_side()][chances[index + 1].message_index[0]], DigMessage):
            just_next.append_effect_calc(
                messages[chance.other_side()][chances[index + 1].message_index[0]: chances[index + 1].message_index[1] + 1], game, "공격종합")
    """

    def select_direct_chance(self, messages):
        chances = self.__class__([])
        for index, chance in enumerate(self):
            if index == len(self) - 1:
                break
            if chance.message_index[0] == chance.message_index[1] \
                and isinstance(messages[chance.side][chance.message_index[0]], ReceiveMessage) \
                and isinstance(messages[chance.other_side()][self[index + 1].message_index[0]], OpenMessage):
                chances.append(chance)

        return chances

    def select_receive_over_chance(self, messages):
        chances = self.__class__([])
        for index, chance in enumerate(self):
            if index == len(self) - 1:
                break
            if chance.message_index[0] == chance.message_index[1] \
                and isinstance(messages[chance.side][chance.message_index[0]], ReceiveMessage) \
                and isinstance(messages[chance.other_side()][self[index + 1].message_index[0]], DigMessage):
                chances.append(chance)

        return chances

    def select_chance_ball_chance(self, messages):
        chances = self.__class__([])
        for index, chance in enumerate(self):
            if index == len(self) - 1:
                break
            if isinstance(messages[chance.side][chance.message_index[1]], DefenseMessage):
                chances.append(chance)

        return chances

    def select_accurate_receive_chance(self, messages):
        chances = self.__class__([])
        for index, chance in enumerate(self):
            if index == len(self) - 1:
                break
            if isinstance(messages[chance.side][chance.message_index[0]], ReceiveMessage)\
                and messages[chance.side][chance.message_index[0]].success_failure == Message.SUCCESS:
                chances.append(chance)

        return chances

    def select_chance_with_message_index(self, index: int) -> Chance:
        for chance in self:
            if index in list(range(chance.message_index[0], chance.message_index[1] + 1)):
                return chance

    def select_near_chance(self, chance: Chance, before_or_after: bool, term: int) -> Chance:
        if before_or_after:
            return self[self.index(chance) - term]
        else:
            return self[self.index(chance) + term]
