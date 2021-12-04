from typing import List
from volleyball.stat.Set import Set


class Rally:
    LEFT = 0
    RIGHT = 1

    def __init__(self, serve: int, rotation: List[List[str]], winner: int, score: List[int], message_index: List[int]):
        self.serve: int = serve
        self.rotation: List[List[str]] = rotation
        self.winner: int = winner
        self.score = score
        self.message_index: List[int] = message_index


class Rallies(List[Rally]):

    def __init__(self, rallies: List[Rally]):
        super(Rallies, self).__init__(rallies)

    def find_near_result(self, index: int, before: int = 0, after: int = 0) -> List[int]:
        return [rally.winner for rally in self[index - before:index + after]]

    def select_rally_with_near_result(self, before_winning_teams: List[int], after_winning_teams : List[int]):
        if after_winning_teams is None:
            after_winning_teams = []
        new_rallies = self.__class__([])
        for rally_index, rally in enumerate(self):
            try:
                before_winning_teams.reverse()
                for i, before_winning_team in enumerate(before_winning_teams):
                    if before_winning_team == self[rally_index - i - 1].winner:
                        continue
                    else:
                        raise IndexError
                for i, after_winning_team in enumerate(after_winning_teams):
                    if after_winning_team == self[rally_index + i + 1]:
                        continue
                    else:
                        raise IndexError
                new_rallies.append(rally)
            except IndexError:
                continue
        return new_rallies

    def select_rally_inner_message_index(self, index: int):
        for rally in self:
            if index in list(range(rally.message_index[0], rally.message_index[1] + 1)):
                return rally

    def select_rally_after_message_index(self, index: int, size: int = 1):
        new_rallies = []
        for i, rally in enumerate(self):
            try:
                if index in list(range(rally.message_index[1], self[i + 1].message_index[0])):
                    for r in range(size):
                        new_rallies.append(self[i + 1 + r])
            except IndexError:
                pass
        return new_rallies

    def select_rally_with_score(self, standard: List[List[int]], set_in_game: Set):
        """한개만 있을 때는 [[최소, 최대, 좌우]], 두개 있을 때는 [[최소, 최대][최소, 최대]]"""
        new_rallies = self.__class__([])
        if len(standard) == 1:
            if set_in_game.index != 4:
                if standard[0][2] == Rally.LEFT:
                    for rally in self:
                        if standard[0][0] <= rally.score[0] <= standard[0][1]:
                            new_rallies.append(rally)
                elif standard[0][2] == Rally.RIGHT:
                    for rally in self:
                        if standard[0][0] <= rally.score[1] <= standard[0][1]:
                            new_rallies.append(rally)
            else:
                if standard[0][2] == Rally.LEFT:
                    for rally in self:
                        if standard[0][0] - 10 <= rally.score[0] <= standard[0][1] - 10:
                            new_rallies.append(rally)
                elif standard[0][2] == Rally.RIGHT:
                    for rally in self:
                        if standard[0][0] - 10 <= rally.score[1] <= standard[0][1] - 10:
                            new_rallies.append(rally)
        else:
            if set_in_game.index != 4:
                for rally in self:
                    if standard[0][0] <= rally.score[0] <= standard[0][1] and standard[1][0] <= rally.score[1] <= standard[1][1]:
                        new_rallies.append(rally)
            else:
                for rally in self:
                    if standard[0][0] - 10 <= rally.score[0] <= standard[0][1] - 10 and standard[0][0] - 10 <= rally.score[1] <= standard[0][1] - 10:
                        new_rallies.append(rally)
        return new_rallies

    def select_rally_with_rotation(self, player_names: List[str], wards: List[bool], left_or_right: int, and_or: bool):
        """player_names:선수 이름, wards: 전위 > True, 후위 > False, and > True, or > False"""
        new_rallies = self.__class__([])
        for rally in self:
            booleans = []
            for i, player_name in enumerate(player_names):
                ward = wards[i]
                if ward:
                    if left_or_right == rally.LEFT:
                        booleans.append(player_name in rally.rotation[0][1:4])
                    elif left_or_right == rally.RIGHT:
                        booleans.append(player_name in rally.rotation[1][1:4])
                else:
                    if left_or_right == rally.LEFT:
                        booleans.append(player_name in rally.rotation[0][4:6] + rally.rotation[0][:1])
                    elif left_or_right == rally.RIGHT:
                        booleans.append(player_name in rally.rotation[1][4:6] + rally.rotation[1][:1])
            if and_or and False not in booleans:
                new_rallies.append(rally)
            elif not and_or and True in booleans:
                new_rallies.append(rally)
        return new_rallies


def rotate_rotation(rotation: List[List[str]], latest_winning_team: int, serve_team: int):
    if latest_winning_team != serve_team:
        if latest_winning_team == Rally.LEFT:
            first_member = rotation[0][0]
            for i, player in enumerate(rotation[0][1:]):
                rotation[0][i] = player
            rotation[0][5] = first_member
        if latest_winning_team == Rally.RIGHT:
            first_member = rotation[1][0]
            for i, player in enumerate(rotation[1][1:]):
                rotation[1][i] = player
            rotation[1][5] = first_member
