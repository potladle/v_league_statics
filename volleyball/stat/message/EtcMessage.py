from volleyball.stat.message.Message import Message


class EtcMessage(Message):

    def __init__(self, index: int, back_num: int, name: str, success_failure : int = 0):
        super(EtcMessage, self).__init__(index, back_num, name, success_failure)


class ExitMessage(EtcMessage):

    def __init__(self, index, back_num: int, name: str, success_failure : int = 0):
        super(ExitMessage, self).__init__(index, back_num, name, success_failure)


class WarningMessage(EtcMessage):

    def __init__(self, index: int, back_num: int = 0, name: str = "", success_failure : int = 0):
        super(WarningMessage, self).__init__(index, back_num, name, success_failure)


class PersonalWarningMessage(EtcMessage):

    def __init__(self, index, back_num: int, name: str, success_failure : int = 0):
        super(PersonalWarningMessage, self).__init__(index, back_num, name, success_failure)


class PenaltyMessage(EtcMessage):

    def __init__(self, index, back_num: int, name: str, success_failure : int = 0):
        super(PenaltyMessage, self).__init__(index, back_num, name, success_failure)


class TimeMessage(EtcMessage):

    def __init__(self, index, back_num: int = 0, name: str = 0, success_failure : int = 0):
        super(TimeMessage, self).__init__(index, back_num, name, success_failure)
