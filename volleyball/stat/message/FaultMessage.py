from volleyball.stat.message.Message import Message


class FaultMessage(Message):

    def __init__(self, index: int, back_num : int = 0, name : str = "팀", success_failure : int = 0):
        super(FaultMessage, self).__init__(index, back_num, name, success_failure)


class PositionFaultMessage (FaultMessage):

    def __init__(self, index: int, back_num : int = 0, name : str = "팀", success_failure : int = 0):
        super(PositionFaultMessage, self).__init__(index, back_num, name, success_failure)


class EtcFaultMessage (FaultMessage):

    def __init__(self, index: int, back_num : int = 0, name : str = "팀", success_failure : int = 0):
        super(EtcFaultMessage, self).__init__(index, back_num, name, success_failure)
