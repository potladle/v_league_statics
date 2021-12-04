from volleyball.stat.message.Message import Message


class AttackMessage(Message):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(AttackMessage, self).__init__(index, back_num, name, success_failure)


class QuickOpenMessage(AttackMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(QuickOpenMessage, self).__init__(index, back_num, name, success_failure)


class OpenMessage(AttackMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(OpenMessage, self).__init__(index, back_num, name, success_failure)


class MoveMessage(AttackMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(MoveMessage, self).__init__(index, back_num, name, success_failure)


class QuickMessage(AttackMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(QuickMessage, self).__init__(index, back_num, name, success_failure)


class TimeLagMessage(AttackMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(TimeLagMessage, self).__init__(index, back_num, name, success_failure)


class BackAttackMessage(AttackMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(BackAttackMessage, self).__init__(index, back_num, name, success_failure)
