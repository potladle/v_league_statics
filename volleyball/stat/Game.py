from typing import List, Dict
from bs4 import Tag, BeautifulSoup


class Game:

    def __init__(self, season, teams, finals, scores, stats, game_num, index):
        self.season: int = season
        self.teams: List[str] = teams
        self.finals: List[int] = finals
        self.scores: List[List[int]] = scores
        self.stats: List[List[Dict[str, List[int]]]] = stats
        self.game_num: int = game_num
        self.index: int = index


def make_team_scores(team_scores: Tag):
    name_and_scores: List[Tag] = team_scores.findAll("td")
    name = name_and_scores[0].text
    final = int(name_and_scores[-1].text)
    scores: List[int] = []

    for score in name_and_scores[1:]:
        scores.append(int(score.text))
        if score.attrs == {"class": ["on"]}:
            break

    return name, final, scores


def make_players_stats(players_stats_tag: Tag):
    players_stats: List[Dict[str, List[int]]] = []
    for player_stats_tag in players_stats_tag.find_all("tr"):
        player_name: str = player_stats_tag.find("td").text
        player_stats: List[int] = []
        for player_stat in player_stats_tag.find_all("td")[1:]:
            player_stats.append(int(player_stat.text))
        players_stats.append({player_name: player_stats})

    return players_stats


def make_game(soup: BeautifulSoup, link: str, index: int) -> Game:
    left_team_scores: Tag = soup.select("#wrp_popup > div.wrp_live_top > article > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1)")[0]
    right_team_scores: Tag = soup.select("#wrp_popup > div.wrp_live_top > article > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(2)")[0]

    left_team, left_final, left_scores = make_team_scores(left_team_scores)
    right_team, right_final, right_scores = make_team_scores(right_team_scores)

    left_players_stats_tag: Tag = soup.select("#wrp_popup > div.wrp_live_bottom > div:nth-child(1) > div > table > tbody")[0]
    right_players_stats_tag: Tag = soup.select("#wrp_popup > div.wrp_live_bottom > div:nth-child(3) > div > table > tbody")[0]

    left_players_stats = make_players_stats(left_players_stats_tag)
    right_players_stats = make_players_stats(right_players_stats_tag)

    season = int(link[53:56])

    try:
        game_num = int(link[-3:])
    except ValueError:
        try:
            game_num = int(link[-2:])
        except ValueError:
            game_num = int(link[-1])

    return Game(season, [left_team, right_team], [left_final, right_final], [left_scores, right_scores], [left_players_stats, right_players_stats], game_num, index)
