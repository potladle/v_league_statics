from volleyball.stat.message.Message import Message


class TeamMessage(Message):

    def __init__(self, index: int, success_failure: int):
        super(TeamMessage, self).__init__(index, 0, "팀", success_failure)
