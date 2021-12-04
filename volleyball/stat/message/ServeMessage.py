from volleyball.stat.message.Message import Message


class ServeMessage(Message):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int,):
        super(ServeMessage, self).__init__(index, back_num, name, success_failure)


class PlotterServeMessage(ServeMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(PlotterServeMessage, self).__init__(index, back_num, name, success_failure)


class SpikeServeMessage(ServeMessage):

    def __init__(self, index: int, back_num: int, name: str, success_failure: int):
        super(SpikeServeMessage, self).__init__(index, back_num, name, success_failure)
