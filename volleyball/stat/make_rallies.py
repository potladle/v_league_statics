from typing import List
from volleyball.stat.Rally import Rally, Rallies, rotate_rotation
from volleyball.stat.message import *
from volleyball.stat.Set import Set
from copy import deepcopy


def make_rallies(messages: List[Messages], set_for_rallies: Set) -> Rallies:
    index = 0
    rallies: List[Rally] = []
    message_index: List[int] = []
    serve = Rally.LEFT
    rotation = deepcopy(set_for_rallies.position)
    score = [0, 0]

    def rally_append(win_side: int):
        message_index.append(index)
        rallies.append(Rally(serve, deepcopy(rotation)
                             , win_side
                             , deepcopy(score)
                             , message_index))
        rotate_rotation(rotation, rallies[len(rallies) - 1].winner, serve)
        score[win_side] = score[win_side] + 1

    while index <= len(messages[0]) - 1:
        left_message = messages[0][index]
        right_message = messages[1][index]

        if index == len(messages[0]) - 1 and type(left_message) == NoneMessage and type(right_message) == NoneMessage:
            break

        if issubclass(type(left_message), ServeMessage):
            message_index.append(index)
            serve = Rally.LEFT

            if len(message_index) == 2:
                print(left_message.__dict__,  messages[1][index + 1].__dict__)
        elif issubclass(type(right_message), ServeMessage):
            message_index.append(index)
            serve = Rally.RIGHT

            if len(message_index) == 2:
                print(right_message.__dict__, messages[0][index + 1].__dict__)

        try:
            next_right_message = messages[1][index + 1]
            next_left_message = messages[0][index + 1]
            if type(left_message) == SubstituteOutMessage:
                idx = rotation[0].index(left_message.name)
                rotation[0][idx] = next_left_message.name
            elif type(right_message) == SubstituteOutMessage:
                idx = rotation[1].index(right_message.name)
                rotation[1][idx] = next_right_message.name
            elif left_message.success_failure != Message.ORDINARY \
                    and (type(left_message) != ReceiveMessage or left_message.success_failure == Message.FAILURE) \
                    and type(next_left_message) != BlockAssistMessage \
                    and ((issubclass(type(next_left_message), ServeMessage) or issubclass(type(next_right_message), ServeMessage))
                         or (next_left_message.success_failure == Message.ORDINARY and next_right_message.success_failure == Message.ORDINARY)):
                rally_append((lambda result: Rally.LEFT if result == Message.SUCCESS else Rally.RIGHT)(
                    left_message.success_failure))
                message_index = []
            elif type(left_message) == BlockAssistMessage:
                rally_append(Rally.LEFT)
                message_index = []
            elif right_message.success_failure != Message.ORDINARY \
                    and (type(right_message) != ReceiveMessage or right_message.success_failure == Message.FAILURE) \
                    and type(next_right_message) != BlockAssistMessage \
                    and ((issubclass(type(next_left_message), ServeMessage) or issubclass(type(next_right_message), ServeMessage))
                         or (next_left_message.success_failure == Message.ORDINARY and next_right_message.success_failure == Message.ORDINARY)):
                rally_append((lambda result: Rally.RIGHT if result == Message.SUCCESS else Rally.LEFT)(
                    right_message.success_failure))
                message_index = []
            elif type(right_message) == BlockAssistMessage:
                rally_append(Rally.RIGHT)
                message_index = []
        except IndexError:
            rally_append(
                (lambda result: Rally.LEFT if result == Message.SUCCESS else Rally.RIGHT)(left_message.success_failure))
            break

        index += 1

    return Rallies(rallies)
