from volleyball.stat.message.Message import Message
from typing import List


class SetMessage(Message):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(SetMessage, self).__init__(index, back_num, name, success_failure)

    def find_next_message(self, list_of_message: List[Message]) -> Message:
        if self.success_failure != Message.FAILURE:
            for message in list_of_message:
                if message.index == self.index + 1:
                    return message
