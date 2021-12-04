from typing import List
from volleyball.stat.message import *
from volleyball.stat.Chance import Chance, Chances
from volleyball.stat.Rally import Rallies


def make_chances(messages: List[Messages], rallies_for_chances: Rallies) -> Chances:
    chances : List[Chance] = []
    side = 0

    for rally in rallies_for_chances:
        try:
            left_rally_messages = messages[0][rally.message_index[0]: rally.message_index[1] + 1]
            right_rally_messages = messages[1][rally.message_index[0]: rally.message_index[1] + 1]

            chance_start_index = rally.message_index[0]
        except IndexError:
            print(len(messages[0]), rally.message_index)

        left_rally_messages = messages[0][rally.message_index[0]: rally.message_index[1] + 1]
        right_rally_messages = messages[1][rally.message_index[0]: rally.message_index[1] + 1]

        chance_start_index = rally.message_index[0]

        for i, _ in enumerate(left_rally_messages):
            left_message: Message = left_rally_messages[i]
            right_message: Message = right_rally_messages[i]

            if not issubclass(type(left_message), NoneMessage) and side == 1:
                chance_start_index = left_message.index
                side = 0
            elif not issubclass(type(right_message), NoneMessage) and side == 0:
                chance_start_index = right_message.index
                side = 1

            if i == len(left_rally_messages) - 1 and side == 0:
                index = len(chances)
                chances.append(Chance(side, left_message.success_failure, [chance_start_index, left_message.index], index))
                break
            elif i == len(right_rally_messages) - 1 and side == 1:
                index = len(chances)
                chances.append(Chance(side, right_message.success_failure, [chance_start_index, right_message.index], index))
                break

            if side == 0 and issubclass(type(left_rally_messages[i + 1]), NoneMessage):
                index = len(chances)
                chances.append(Chance(side, Chance.CONTINUE, [chance_start_index, left_message.index], index))
            elif side == 1 and issubclass(type(right_rally_messages[i + 1]), NoneMessage):
                index = len(chances)
                chances.append(Chance(side, Chance.CONTINUE, [chance_start_index, right_message.index], index))

    return Chances(chances)
