from volleyball.stat.message.Message import Message


class BlockingMessage(Message):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(BlockingMessage, self).__init__(index, back_num, name, success_failure)


class BlockMessage(BlockingMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(BlockMessage, self).__init__(index, back_num, name, success_failure)


class EffectiveBlockMessage(BlockingMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int = 0):
        super(EffectiveBlockMessage, self).__init__(index, back_num, name, success_failure)


class BlockAssistMessage(BlockingMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int = 0,):
        super(BlockAssistMessage, self).__init__(index, back_num, name, success_failure)
